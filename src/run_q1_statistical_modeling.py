from pathlib import Path
import pandas as pd
import numpy as np


INPUT_SOURCES = [
    {
        "name": "v6_job_roles",
        "root": Path("results/occupational_benchmark_v6_job_roles_large_all_models"),
        "pattern": "scoring_*/*.csv",
    },
    {
        "name": "arabjobs_v7",
        "root": Path("results/external_datasets/arabjobs"),
        "pattern": "scoring_*/*.csv",
    },
]

OUTPUT_DIR = Path("results/q1_statistical_modeling")
DOC_PATH = Path("docs/occupational_scope/q1_statistical_modeling_summary.md")


def load_scoring_outputs():
    frames = []

    for source in INPUT_SOURCES:
        root = source["root"]
        if not root.exists():
            continue

        for path in root.glob(source["pattern"]):
            df = pd.read_csv(path, encoding="utf-8-sig")
            if "score_difference" not in df.columns or "preferred_gender" not in df.columns:
                continue

            df = df.copy()
            df["dataset_source"] = source["name"]

            for col in [
                "model_name",
                "field",
                "department",
                "job_family",
                "seniority_level",
                "job_role_type",
                "template_type",
                "semantic_frame",
                "dialect",
                "score_difference",
                "preferred_gender",
            ]:
                if col not in df.columns:
                    df[col] = "unknown"

            frames.append(df)

    if not frames:
        raise RuntimeError("No valid scoring outputs found.")

    return pd.concat(frames, ignore_index=True)


def summarize_factor(df, factor):
    rows = []

    for (source, model, value), group in df.groupby(["dataset_source", "model_name", factor]):
        total = len(group)
        m_count = int((group["preferred_gender"] == "masculine").sum())
        f_count = int((group["preferred_gender"] == "feminine").sum())
        e_count = int((group["preferred_gender"] == "equal").sum())

        rows.append({
            "dataset_source": source,
            "model_name": model,
            factor: value,
            "total_items": total,
            "masculine_preferred_count": m_count,
            "feminine_preferred_count": f_count,
            "equal_count": e_count,
            "masculine_preferred_percent": round((m_count / total) * 100, 6),
            "feminine_preferred_percent": round((f_count / total) * 100, 6),
            "equal_percent": round((e_count / total) * 100, 6),
            "average_score_difference": group["score_difference"].astype(float).mean(),
            "median_score_difference": group["score_difference"].astype(float).median(),
            "std_score_difference": group["score_difference"].astype(float).std(),
        })

    return pd.DataFrame(rows)


def calculate_effect_strength(df, factor):
    """
    Non-parametric publication-friendly effect summary:
    how much average score_difference varies across levels of a factor.
    """
    rows = []

    for source, source_group in df.groupby("dataset_source"):
        if factor not in source_group.columns:
            continue

        factor_means = (
            source_group
            .groupby(factor)["score_difference"]
            .mean()
            .dropna()
        )

        if len(factor_means) < 2:
            continue

        rows.append({
            "dataset_source": source,
            "factor": factor,
            "num_levels": len(factor_means),
            "min_group_mean": factor_means.min(),
            "max_group_mean": factor_means.max(),
            "range_of_group_means": factor_means.max() - factor_means.min(),
            "std_of_group_means": factor_means.std(),
            "strongest_feminine_level": factor_means.idxmin(),
            "strongest_masculine_level": factor_means.idxmax(),
        })

    return rows


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_scoring_outputs()
    df["score_difference"] = pd.to_numeric(df["score_difference"], errors="coerce")
    df = df.dropna(subset=["score_difference"])

    df["is_masculine_preferred"] = (df["preferred_gender"] == "masculine").astype(int)

    combined_path = OUTPUT_DIR / "q1_combined_scoring_outputs_v6_arabjobs.csv"
    df.to_csv(combined_path, index=False, encoding="utf-8-sig")

    factors = [
        "dataset_source",
        "model_name",
        "field",
        "department",
        "job_family",
        "seniority_level",
        "job_role_type",
        "template_type",
        "semantic_frame",
        "dialect",
    ]

    effect_rows = []

    for factor in factors:
        if factor not in df.columns:
            continue

        summary = summarize_factor(df, factor)
        summary.to_csv(OUTPUT_DIR / f"summary_by_{factor}.csv", index=False, encoding="utf-8-sig")

        if factor not in ["dataset_source"]:
            effect_rows.extend(calculate_effect_strength(df, factor))

    effect_df = pd.DataFrame(effect_rows)
    effect_df = effect_df.sort_values(
        ["dataset_source", "range_of_group_means"],
        ascending=[True, False],
    )
    effect_df.to_csv(OUTPUT_DIR / "q1_factor_effect_strength_summary.csv", index=False, encoding="utf-8-sig")

    overall = summarize_factor(df, "dataset_source")
    overall.to_csv(OUTPUT_DIR / "q1_overall_by_dataset_source_and_model.csv", index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# Q1 Statistical Modeling and Factor Sensitivity Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This analysis strengthens the publication version by comparing gender-preference scores across "
        "controlled v6 job-role data and ArabJobs v7 real-world job-ad data."
    )
    doc.append("")
    doc.append("## Inputs")
    doc.append("")
    doc.append("- v6 expanded job-role scoring outputs")
    doc.append("- ArabJobs v7 external real-world job-ad scoring outputs")
    doc.append("")
    doc.append("## Output Files")
    doc.append("")
    doc.append(f"- Combined scoring file: `{combined_path}`")
    doc.append(f"- Overall by dataset and model: `{OUTPUT_DIR / 'q1_overall_by_dataset_source_and_model.csv'}`")
    doc.append(f"- Factor sensitivity summary: `{OUTPUT_DIR / 'q1_factor_effect_strength_summary.csv'}`")
    doc.append("")
    doc.append("## Factor Sensitivity Interpretation")
    doc.append("")
    doc.append(
        "For each factor, the analysis computes the range of average score_difference across factor levels. "
        "A larger range indicates that measured gender preference is more sensitive to that factor."
    )
    doc.append("")

    if not effect_df.empty:
        doc.append("## Strongest Factor Effects")
        doc.append("")
        for source, group in effect_df.groupby("dataset_source"):
            doc.append(f"### {source}")
            doc.append("")
            top = group.head(8)
            for _, row in top.iterrows():
                doc.append(
                    f"- {row['factor']}: range={row['range_of_group_means']}, "
                    f"strongest feminine={row['strongest_feminine_level']}, "
                    f"strongest masculine={row['strongest_masculine_level']}"
                )
            doc.append("")

    doc.append("## Publication Claim")
    doc.append("")
    doc.append(
        "This analysis supports the claim that Arabic occupational gender-bias measurement is sensitive "
        "to dataset source, model choice, template formulation, dialect, department, job family, seniority, "
        "and job-role framing."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("Q1 statistical modeling completed.")
    print("Output dir:", OUTPUT_DIR)
    print("Doc:", DOC_PATH)
    print("")
    print("Overall:")
    print(overall.to_string(index=False))
    print("")
    print("Top factor effects:")
    print(effect_df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()