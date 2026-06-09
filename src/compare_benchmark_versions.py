from pathlib import Path
import pandas as pd


RESULTS_DIR = Path("results")
OUTPUT_PATH = RESULTS_DIR / "benchmark_version_comparison.csv"


VERSIONS = ["v03", "v04", "v05"]


def read_first_row(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    return df.iloc[0].to_dict()


def count_warnings(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    if "warnings" not in df.columns:
        return None

    warning_rows = df[df["warnings"] != "ok"]
    return len(warning_rows)


def main():
    rows = []

    for version in VERSIONS:
        summary_path = RESULTS_DIR / f"analysis_summary_{version}.csv"
        dialect_path = RESULTS_DIR / f"analysis_by_dialect_{version}.csv"
        template_quality_path = RESULTS_DIR / f"quality_by_template_id_{version}.csv"
        concept_quality_path = RESULTS_DIR / f"quality_by_concept_id_{version}.csv"

        summary = read_first_row(summary_path)

        dialect_df = pd.read_csv(dialect_path, encoding="utf-8-sig")

        egyptian_avg = dialect_df.loc[
            dialect_df["dialect"] == "Egyptian",
            "average_score_difference"
        ].iloc[0]

        msa_avg = dialect_df.loc[
            dialect_df["dialect"] == "MSA",
            "average_score_difference"
        ].iloc[0]

        dialect_gap = abs(egyptian_avg - msa_avg)

        template_warnings = count_warnings(template_quality_path)
        concept_warnings = count_warnings(concept_quality_path)

        rows.append({
            "version": version,
            "total_items": summary["total_items"],
            "masculine_preferred_count": summary["masculine_preferred_count"],
            "feminine_preferred_count": summary["feminine_preferred_count"],
            "masculine_preferred_percent": summary["masculine_preferred_percent"],
            "feminine_preferred_percent": summary["feminine_preferred_percent"],
            "overall_average_score_difference": summary["average_score_difference"],
            "overall_median_score_difference": summary["median_score_difference"],
            "egyptian_average_score_difference": egyptian_avg,
            "msa_average_score_difference": msa_avg,
            "absolute_dialect_gap": dialect_gap,
            "template_warning_count": template_warnings,
            "concept_warning_count": concept_warnings,
        })

    comparison_df = pd.DataFrame(rows)

    comparison_df["recommended_role"] = comparison_df["version"].map({
        "v03": "earlier pilot with template effects",
        "v04": "stable pilot baseline",
        "v05": "cleaning ablation, not selected as baseline",
    })

    comparison_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Benchmark version comparison saved to:")
    print(OUTPUT_PATH)

    print("\nComparison:")
    print(comparison_df)


if __name__ == "__main__":
    main()