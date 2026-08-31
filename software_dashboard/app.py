from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Arabic Occupational Gender Bias Dashboard",
    page_icon="📊",
    layout="wide",
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


DATASET_PATHS = {
    "v2 main benchmark": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v2.csv",
    "v4 template perturbation": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv",
    "v5 job titles": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v5_job_titles.csv",
    "v6 job roles and departments": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv",
    "ArabJobs v7 external": PROJECT_ROOT / "data/external_datasets/arabjobs/arabjobs_v7_counterfactual_pairs.csv",
}


RESULT_PATHS = {
    "v2 all models": PROJECT_ROOT / "results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv",
    "v4 all models": PROJECT_ROOT / "results/occupational_benchmark_v4_template_perturbation_all_models/combined_analysis/overall_by_model.csv",
    "v6 large all models": PROJECT_ROOT / "results/occupational_benchmark_v6_job_roles_large_all_models/combined_analysis/v6_overall_by_model.csv",
    "ArabJobs v7": PROJECT_ROOT / "results/external_datasets/arabjobs/combined_analysis/arabjobs_v7_overall_by_model.csv",
}


VALIDATION_PATHS = {
    "Score difference validation": PROJECT_ROOT / "results/final_package/score_difference_validation_report.csv",
    "Q1 token length control": PROJECT_ROOT / "results/q1_token_length_control/q1_token_length_control_summary.csv",
    "Q1 factor sensitivity": PROJECT_ROOT / "results/q1_statistical_modeling/q1_factor_effect_strength_summary.csv",
    "Q1 cross benchmark contrast": PROJECT_ROOT / "results/q1_cross_benchmark_contrast/q1_cross_benchmark_overall_contrast.csv",
    "Q1 human validation sampling": PROJECT_ROOT / "results/human_validation/q1_validation/q1_human_validation_sampling_summary.csv",
    "Q1 human validation agreement": PROJECT_ROOT / "results/human_validation/q1_validation/q1_human_validation_agreement_summary.csv",
}


def read_csv_safe(path: Path):
    if not path.exists():
        return None
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return pd.read_csv(path)


def classify_direction(value):
    try:
        value = float(value)
    except Exception:
        return "unknown"

    if value > 0.05:
        return "masculine"
    if value < -0.05:
        return "feminine"
    return "near-neutral / mixed"


def show_metric_cards(df):
    total_rows = len(df)
    total_cols = len(df.columns)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", f"{total_rows:,}")
    c2.metric("Columns", f"{total_cols:,}")

    if "template_id" in df.columns:
        c3.metric("Templates", f"{df['template_id'].nunique():,}")
    else:
        c3.metric("Templates", "N/A")

    if "model_name" in df.columns:
        c4.metric("Models", f"{df['model_name'].nunique():,}")
    elif "role_id" in df.columns:
        c4.metric("Roles", f"{df['role_id'].nunique():,}")
    elif "occupation_key" in df.columns:
        c4.metric("Occupations", f"{df['occupation_key'].nunique():,}")
    else:
        c4.metric("Unique items", "N/A")


def show_dataset_page():
    st.header("Dataset Explorer")

    dataset_name = st.selectbox("Choose dataset", list(DATASET_PATHS.keys()))
    path = DATASET_PATHS[dataset_name]

    st.caption(str(path))

    df = read_csv_safe(path)

    if df is None:
        st.error("Dataset file not found.")
        return

    show_metric_cards(df)

    st.subheader("Dataset preview")
    st.dataframe(df.head(100), use_container_width=True)

    st.subheader("Dataset structure")

    structure_rows = []

    for col in [
        "benchmark_version",
        "field",
        "department",
        "job_family",
        "seniority_level",
        "job_role_type",
        "template_id",
        "template_type",
        "semantic_frame",
        "dialect",
        "country",
        "job_category",
        "sub_category",
    ]:
        if col in df.columns:
            structure_rows.append({
                "column": col,
                "unique_values": df[col].nunique(dropna=True),
                "missing_values": df[col].isna().sum(),
            })

    if structure_rows:
        st.dataframe(pd.DataFrame(structure_rows), use_container_width=True)

    st.subheader("Distribution charts")

    chart_cols = [
        "field",
        "department",
        "dialect",
        "template_type",
        "semantic_frame",
        "seniority_level",
        "job_role_type",
        "country",
        "job_category",
    ]

    available_chart_cols = [c for c in chart_cols if c in df.columns]

    if available_chart_cols:
        selected_col = st.selectbox("Group by", available_chart_cols)
        counts = df[selected_col].fillna("unknown").value_counts().reset_index()
        counts.columns = [selected_col, "count"]

        fig = px.bar(
            counts,
            x=selected_col,
            y="count",
            title=f"Distribution by {selected_col}",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No categorical columns available for charts.")

    st.subheader("Sentence examples")

    if "masculine_sentence" in df.columns and "feminine_sentence" in df.columns:
        sample = df.sample(min(10, len(df)), random_state=42)
        st.dataframe(
            sample[
                [
                    c for c in [
                        "id",
                        "field",
                        "department",
                        "template_id",
                        "dialect",
                        "masculine_sentence",
                        "feminine_sentence",
                    ]
                    if c in sample.columns
                ]
            ],
            use_container_width=True,
        )


def show_results_page():
    st.header("Model Results")

    result_name = st.selectbox("Choose result table", list(RESULT_PATHS.keys()))
    path = RESULT_PATHS[result_name]

    st.caption(str(path))

    df = read_csv_safe(path)

    if df is None:
        st.error("Result file not found.")
        return

    if "average_score_difference" in df.columns:
        df["direction"] = df["average_score_difference"].apply(classify_direction)

    show_metric_cards(df)

    st.subheader("Overall results")
    st.dataframe(df, use_container_width=True)

    if "model_name" in df.columns and "average_score_difference" in df.columns:
        st.subheader("Average score difference by model")

        fig = px.bar(
            df,
            x="model_name",
            y="average_score_difference",
            color="direction" if "direction" in df.columns else None,
            title="Average score_difference by model",
        )
        fig.add_hline(y=0)
        st.plotly_chart(fig, use_container_width=True)

    if all(c in df.columns for c in ["model_name", "masculine_preferred_percent", "feminine_preferred_percent"]):
        st.subheader("Masculine vs feminine preference percentage")

        melted = df.melt(
            id_vars=["model_name"],
            value_vars=["masculine_preferred_percent", "feminine_preferred_percent"],
            var_name="preference",
            value_name="percent",
        )

        fig = px.bar(
            melted,
            x="model_name",
            y="percent",
            color="preference",
            barmode="group",
            title="Preference percentages by model",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_cross_benchmark_page():
    st.header("Cross-Benchmark Comparison")

    path = PROJECT_ROOT / "results/q1_cross_benchmark_contrast/q1_cross_benchmark_overall_contrast.csv"
    df = read_csv_safe(path)

    if df is None:
        st.error("Cross-benchmark contrast file not found.")
        return

    st.dataframe(df, use_container_width=True)

    if all(c in df.columns for c in ["benchmark", "model_name", "average_score_difference"]):
        st.subheader("Average score difference across benchmarks")

        fig = px.bar(
            df,
            x="benchmark",
            y="average_score_difference",
            color="model_name",
            barmode="group",
            title="Cross-benchmark average score_difference",
        )
        fig.add_hline(y=0)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Direction changes")

    if all(c in df.columns for c in ["model_name", "direction"]):
        rows = []
        for model, group in df.groupby("model_name"):
            directions = sorted(group["direction"].dropna().unique().tolist())
            rows.append({
                "model_name": model,
                "benchmarks_covered": group["benchmark"].nunique(),
                "directions_observed": ", ".join(directions),
                "direction_changed": len(directions) > 1,
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True)


def show_validation_page():
    st.header("Validation and Robustness")

    validation_name = st.selectbox("Choose validation output", list(VALIDATION_PATHS.keys()))
    path = VALIDATION_PATHS[validation_name]

    st.caption(str(path))

    df = read_csv_safe(path)

    if df is None:
        st.error("Validation file not found.")
        return

    show_metric_cards(df)

    st.dataframe(df, use_container_width=True)

    if "status" in df.columns:
        st.subheader("Validation status")
        counts = df["status"].value_counts().reset_index()
        counts.columns = ["status", "count"]
        fig = px.bar(counts, x="status", y="count", title="Validation status counts")
        st.plotly_chart(fig, use_container_width=True)

    if "cohens_kappa" in df.columns:
        st.subheader("Cohen's Kappa")
        fig = px.bar(
            df,
            x="validation_field",
            y="cohens_kappa",
            title="Human validation Cohen's Kappa",
        )
        st.plotly_chart(fig, use_container_width=True)

    if "range_of_group_means" in df.columns:
        st.subheader("Factor sensitivity")
        fig = px.bar(
            df.head(30),
            x="factor",
            y="range_of_group_means",
            color="dataset_source" if "dataset_source" in df.columns else None,
            title="Top factor sensitivity ranges",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_model_command_page():
    st.header("Scoring Command Generator")

    dataset_options = {
        "v2": "data/occupational_benchmark/occupational_bias_v2.csv",
        "v4": "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv",
        "v5": "data/occupational_benchmark/occupational_bias_v5_job_titles.csv",
        "v6": "data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv",
        "ArabJobs v7": "data/external_datasets/arabjobs/arabjobs_v7_counterfactual_pairs.csv",
    }

    model_options = [
        "aubmindlab/aragpt2-base",
        "aubmindlab/aragpt2-medium",
        "bigscience/bloom-560m",
        "bigscience/bloom-1b1",
        "facebook/xglm-564M",
        "Qwen/Qwen2.5-0.5B",
    ]

    dataset_label = st.selectbox("Dataset", list(dataset_options.keys()))
    model_name = st.selectbox("Model", model_options)

    safe_name = model_name.replace("/", "_").replace("-", "_").replace(".", "_")
    out_dir = f"results/software_runs/{dataset_label.lower().replace(' ', '_')}/scoring_{safe_name}"

    command = f"""python src/score_occupational_single_model_v1.py `
  --input {dataset_options[dataset_label]} `
  --model_name {model_name} `
  --output_dir {out_dir}"""

    st.subheader("PowerShell scoring command")
    st.code(command, language="powershell")

    analysis_command = f"""python src/analyze_occupational_results_v1.py `
  --input {out_dir}/scoring_results_occupational_v1_{safe_name}.csv `
  --output_dir {out_dir.replace("scoring_", "analysis_")}"""

    st.subheader("PowerShell analysis command")
    st.code(analysis_command, language="powershell")


def show_about_page():
    st.header("About This Software")

    st.markdown(
        """
        This dashboard supports the thesis project:

        **Measuring Occupational Gender Bias in Arabic Causal Language Models using a Counterfactual Dialect-Aware Benchmark**

        The software provides an interface for inspecting datasets, viewing model results, comparing benchmark versions,
        validating score-difference outputs, and preparing publication-ready evidence.

        Main score:

        `score_difference = masculine_score - feminine_score`

        Interpretation:

        - Positive score_difference: masculine variant preferred
        - Negative score_difference: feminine variant preferred
        - Zero score_difference: equal preference

        Main software modules:

        - Dataset explorer
        - Model result dashboard
        - Cross-benchmark comparison
        - Validation and robustness dashboard
        - Scoring command generator
        """
    )


st.sidebar.title("Arabic Bias Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "About",
        "Dataset Explorer",
        "Model Results",
        "Cross-Benchmark Comparison",
        "Validation and Robustness",
        "Scoring Command Generator",
    ],
)

if page == "About":
    show_about_page()
elif page == "Dataset Explorer":
    show_dataset_page()
elif page == "Model Results":
    show_results_page()
elif page == "Cross-Benchmark Comparison":
    show_cross_benchmark_page()
elif page == "Validation and Robustness":
    show_validation_page()
elif page == "Scoring Command Generator":
    show_model_command_page()