from pathlib import Path
import subprocess
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Arabic Bias Measurement Software",
    page_icon="⚖️",
    layout="wide",
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCORER_SCRIPT = PROJECT_ROOT / "src" / "score_occupational_single_model_v1.py"
ANALYZER_SCRIPT = PROJECT_ROOT / "src" / "analyze_occupational_results_v1.py"

DEFAULT_MODELS = [
    "aubmindlab/aragpt2-base",
    "aubmindlab/aragpt2-medium",
    "bigscience/bloom-560m",
    "bigscience/bloom-1b1",
    "facebook/xglm-564M",
    "Qwen/Qwen2.5-0.5B",
]

BENCHMARKS = {
    "v2 main benchmark": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v2.csv",
    "v4 template perturbation": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv",
    "v5 job titles": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v5_job_titles.csv",
    "v6 job roles and departments": PROJECT_ROOT / "data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv",
    "ArabJobs v7 external": PROJECT_ROOT / "data/external_datasets/arabjobs/arabjobs_v7_counterfactual_pairs.csv",
}


def safe_slug(text: str) -> str:
    return (
        text.replace("/", "_")
        .replace("\\", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace(" ", "_")
    )


def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return pd.read_csv(path)


def classify_direction(value):
    value = float(value)
    if value > 0:
        return "masculine"
    if value < 0:
        return "feminine"
    return "equal"


def run_command(command):
    result = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        shell=False,
    )
    return result


def find_scoring_output(output_dir: Path):
    files = list(output_dir.glob("scoring_results_occupational_v1_*.csv"))
    if not files:
        return None
    return files[0]


def page_about():
    st.title("Arabic Occupational Gender Bias Measurement Software")

    st.markdown(
        """
This software measures Arabic occupational gender bias using masculine–feminine counterfactual sentence pairs.

Main equation:

`score_difference = masculine_score - feminine_score`

Interpretation:

- Positive score_difference = masculine preference
- Negative score_difference = feminine preference
- Zero score_difference = equal preference
"""
    )


def page_single_pair():
    st.header("Measure One Sentence Pair")

    masculine_sentence = st.text_area(
        "Masculine sentence",
        value="هذا الطبيب يعمل في المستشفى.",
        height=120,
    )

    feminine_sentence = st.text_area(
        "Feminine sentence",
        value="هذه الطبيبة تعمل في المستشفى.",
        height=120,
    )

    model_name = st.selectbox("Model", DEFAULT_MODELS)

    if st.button("Measure Bias", type="primary"):
        temp_dir = PROJECT_ROOT / "results/software_bias_measurement/temp_single_pair"
        temp_dir.mkdir(parents=True, exist_ok=True)

        input_path = temp_dir / "single_pair_input.csv"
        output_dir = temp_dir / f"scoring_{safe_slug(model_name)}"

        input_df = pd.DataFrame(
            [
                {
                    "id": "single_pair_001",
                    "field": "manual_input",
                    "template_id": "manual_input",
                    "dialect": "unspecified",
                    "masculine_sentence": masculine_sentence,
                    "feminine_sentence": feminine_sentence,
                }
            ]
        )

        input_df.to_csv(input_path, index=False, encoding="utf-8-sig")

        command = [
            "python",
            str(SCORER_SCRIPT),
            "--input",
            str(input_path),
            "--model_name",
            model_name,
            "--output_dir",
            str(output_dir),
        ]

        with st.spinner("Running scorer..."):
            result = run_command(command)

        if result.returncode != 0:
            st.error("Scoring failed.")
            st.code(result.stderr or result.stdout)
            return

        scoring_file = find_scoring_output(output_dir)

        if scoring_file is None:
            st.error("Scoring finished, but no output CSV was found.")
            st.code(result.stdout)
            return

        scored = read_csv_safe(scoring_file)

        st.success("Bias measurement completed.")
        st.dataframe(scored, use_container_width=True)

        row = scored.iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Masculine score", round(float(row["masculine_score"]), 6))
        c2.metric("Feminine score", round(float(row["feminine_score"]), 6))
        c3.metric("Score difference", round(float(row["score_difference"]), 6))
        c4.metric("Preferred gender", row["preferred_gender"])

        chart_df = pd.DataFrame(
            {
                "variant": ["masculine", "feminine"],
                "score": [row["masculine_score"], row["feminine_score"]],
            }
        )

        fig = px.bar(chart_df, x="variant", y="score", title="Sentence scores")
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "Download result CSV",
            data=scored.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            file_name="single_pair_bias_result.csv",
            mime="text/csv",
        )


def page_csv():
    st.header("Measure Uploaded CSV")

    st.markdown("Required columns: `masculine_sentence`, `feminine_sentence`")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    model_name = st.selectbox("Model", DEFAULT_MODELS, key="csv_model")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
        st.dataframe(df.head(20), use_container_width=True)

        missing = [c for c in ["masculine_sentence", "feminine_sentence"] if c not in df.columns]
        if missing:
            st.error(f"Missing required columns: {missing}")
            return

        max_rows = st.number_input(
            "Maximum rows to score",
            min_value=1,
            max_value=len(df),
            value=min(20, len(df)),
            step=1,
        )

        if st.button("Run Bias Measurement", type="primary"):
            temp_dir = PROJECT_ROOT / "results/software_bias_measurement/temp_uploaded_csv"
            temp_dir.mkdir(parents=True, exist_ok=True)

            input_path = temp_dir / "uploaded_input.csv"
            output_dir = temp_dir / f"scoring_{safe_slug(model_name)}"

            df.head(int(max_rows)).to_csv(input_path, index=False, encoding="utf-8-sig")

            command = [
                "python",
                str(SCORER_SCRIPT),
                "--input",
                str(input_path),
                "--model_name",
                model_name,
                "--output_dir",
                str(output_dir),
            ]

            with st.spinner("Running scorer..."):
                result = run_command(command)

            if result.returncode != 0:
                st.error("Scoring failed.")
                st.code(result.stderr or result.stdout)
                return

            scoring_file = find_scoring_output(output_dir)

            if scoring_file is None:
                st.error("Scoring finished, but no output CSV was found.")
                st.code(result.stdout)
                return

            scored = read_csv_safe(scoring_file)

            st.success("Bias measurement completed.")
            st.dataframe(scored, use_container_width=True)

            counts = scored["preferred_gender"].value_counts().reset_index()
            counts.columns = ["preferred_gender", "count"]

            fig = px.bar(counts, x="preferred_gender", y="count", title="Preferred gender distribution")
            st.plotly_chart(fig, use_container_width=True)

            st.download_button(
                "Download result CSV",
                data=scored.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
                file_name="uploaded_csv_bias_results.csv",
                mime="text/csv",
            )


def page_project_benchmark():
    st.header("Measure Project Benchmark")

    benchmark_name = st.selectbox("Benchmark", list(BENCHMARKS.keys()))
    model_name = st.selectbox("Model", DEFAULT_MODELS, key="bench_model")

    path = BENCHMARKS[benchmark_name]
    st.caption(str(path))

    if not path.exists():
        st.error("Benchmark file not found.")
        return

    df = read_csv_safe(path)
    st.dataframe(df.head(20), use_container_width=True)

    max_rows = st.number_input(
        "Maximum rows to score",
        min_value=1,
        max_value=len(df),
        value=min(20, len(df)),
        step=1,
    )

    if st.button("Run Benchmark Measurement", type="primary"):
        temp_dir = PROJECT_ROOT / "results/software_bias_measurement/temp_project_benchmark"
        temp_dir.mkdir(parents=True, exist_ok=True)

        input_path = temp_dir / f"{safe_slug(benchmark_name)}_input.csv"
        output_dir = temp_dir / f"scoring_{safe_slug(model_name)}"

        df.head(int(max_rows)).to_csv(input_path, index=False, encoding="utf-8-sig")

        command = [
            "python",
            str(SCORER_SCRIPT),
            "--input",
            str(input_path),
            "--model_name",
            model_name,
            "--output_dir",
            str(output_dir),
        ]

        with st.spinner("Running scorer..."):
            result = run_command(command)

        if result.returncode != 0:
            st.error("Scoring failed.")
            st.code(result.stderr or result.stdout)
            return

        scoring_file = find_scoring_output(output_dir)

        if scoring_file is None:
            st.error("Scoring finished, but no output CSV was found.")
            st.code(result.stdout)
            return

        scored = read_csv_safe(scoring_file)

        st.success("Benchmark measurement completed.")
        st.dataframe(scored, use_container_width=True)

        total = len(scored)
        masculine = int((scored["preferred_gender"] == "masculine").sum())
        feminine = int((scored["preferred_gender"] == "feminine").sum())
        equal = int((scored["preferred_gender"] == "equal").sum())
        avg_diff = float(scored["score_difference"].mean())

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total", total)
        c2.metric("Masculine", masculine)
        c3.metric("Feminine", feminine)
        c4.metric("Equal", equal)
        c5.metric("Average diff", round(avg_diff, 6))

        counts = scored["preferred_gender"].value_counts().reset_index()
        counts.columns = ["preferred_gender", "count"]

        fig = px.bar(counts, x="preferred_gender", y="count", title="Preferred gender distribution")
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "Download result CSV",
            data=scored.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            file_name="benchmark_bias_results.csv",
            mime="text/csv",
        )


def page_command_generator():
    st.header("Command Generator")

    benchmark_name = st.selectbox("Benchmark", list(BENCHMARKS.keys()), key="cmd_bench")
    model_name = st.selectbox("Model", DEFAULT_MODELS, key="cmd_model")

    input_path = BENCHMARKS[benchmark_name]
    output_dir = f"results/software_bias_measurement/{safe_slug(benchmark_name)}/scoring_{safe_slug(model_name)}"

    command = f"""python src/score_occupational_single_model_v1.py `
  --input {input_path.relative_to(PROJECT_ROOT)} `
  --model_name {model_name} `
  --output_dir {output_dir}"""

    st.code(command, language="powershell")


page = st.sidebar.radio(
    "Navigation",
    [
        "About",
        "Measure one pair",
        "Measure uploaded CSV",
        "Measure project benchmark",
        "Command generator",
    ],
)

if page == "About":
    page_about()
elif page == "Measure one pair":
    page_single_pair()
elif page == "Measure uploaded CSV":
    page_csv()
elif page == "Measure project benchmark":
    page_project_benchmark()
elif page == "Command generator":
    page_command_generator()