from pathlib import Path
import pandas as pd


DOC_PATH = Path("docs/occupational_scope/final_external_dataset_expansion_summary.md")

ARABJOBS_SUMMARY = Path("results/external_datasets/arabjobs/combined_analysis/arabjobs_v7_overall_by_model.csv")
V6_SUMMARY = Path("results/occupational_benchmark_v6_job_roles_large_all_models/combined_analysis/v6_overall_by_model.csv")


def add_table_summary(doc, title, path):
    doc.append(f"## {title}")
    doc.append("")

    if not path.exists():
        doc.append(f"Missing file: `{path}`")
        doc.append("")
        return

    df = pd.read_csv(path, encoding="utf-8-sig")

    for _, row in df.iterrows():
        direction_col = None
        for col in ["v6_direction", "arabjobs_v7_direction"]:
            if col in df.columns:
                direction_col = col

        doc.append(f"### {row['model_name']}")
        doc.append("")
        doc.append(f"- Total items: {row['total_items']}")
        doc.append(f"- Masculine preferred: {row['masculine_preferred_count']} ({row['masculine_preferred_percent']}%)")
        doc.append(f"- Feminine preferred: {row['feminine_preferred_count']} ({row['feminine_preferred_percent']}%)")
        doc.append(f"- Equal: {row['equal_count']} ({row['equal_percent']}%)")
        doc.append(f"- Average score difference: {row['average_score_difference']}")
        doc.append(f"- Median score difference: {row['median_score_difference']}")
        if direction_col:
            doc.append(f"- Direction: {row[direction_col]}")
        doc.append("")


def main():
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    doc = []
    doc.append("# Final External Dataset Expansion Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This document summarizes the expanded real-world and job-role dataset components added to strengthen the Arabic occupational gender-bias evaluation framework."
    )
    doc.append("")

    doc.append("## Added Dataset Components")
    doc.append("")
    doc.append("### v6 Expanded Job Roles and Departments")
    doc.append("")
    doc.append("- Controlled expanded benchmark")
    doc.append("- 120 structured job roles")
    doc.append("- 24 templates")
    doc.append("- 2,880 masculine-feminine counterfactual pairs per model")
    doc.append("- Dimensions: department, job family, seniority level, job-role type, workplace context, template type, semantic frame, and dialect")
    doc.append("")
    doc.append("### ArabJobs v7 External Real-World Job Ads")
    doc.append("")
    doc.append("- External real-world Arabic job-ad corpus")
    doc.append("- Derived counterfactual sentence pairs from matched job titles and recruitment metadata")
    doc.append("- Includes country, job category, sub-category, profession, original gender label, and original job title metadata")
    doc.append("- Used as external validation beyond controlled templates")
    doc.append("")

    add_table_summary(doc, "v6 Overall Model Results", V6_SUMMARY)
    add_table_summary(doc, "ArabJobs v7 Overall Model Results", ARABJOBS_SUMMARY)

    doc.append("## Main Interpretation")
    doc.append("")
    doc.append(
        "The v6 and ArabJobs v7 extensions strengthen the thesis by showing that Arabic occupational gender-bias measurements are sensitive to the form of the evaluation data. Controlled job-role templates and real-world recruitment-language contexts can produce different measured gender-preference directions, demonstrating the importance of robustness-oriented benchmark design."
    )
    doc.append("")

    doc.append("## Publication Value")
    doc.append("")
    doc.append(
        "These additions improve Q1-readiness by expanding the work from a controlled benchmark study into a broader evaluation framework that includes structured labor-market dimensions and external real-world Arabic job-ad validation."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")
    print("Created:", DOC_PATH)


if __name__ == "__main__":
    main()