from pathlib import Path
import pandas as pd


SOURCES = [
    ("v2_main", Path("results/occupational_benchmark_v2_all_models/combined_analysis/overall_by_model.csv")),
    ("v4_template_perturbation", Path("results/occupational_benchmark_v4_template_perturbation_all_models/combined_analysis/overall_by_model.csv")),
    ("v5_job_titles", Path("results/occupational_benchmark_v5_job_titles_quick_models/combined_analysis/overall_by_model.csv")),
    ("v6_job_roles", Path("results/occupational_benchmark_v6_job_roles_large_all_models/combined_analysis/v6_overall_by_model.csv")),
    ("arabjobs_v7_real_world", Path("results/external_datasets/arabjobs/combined_analysis/arabjobs_v7_overall_by_model.csv")),
]

OUTPUT_DIR = Path("results/q1_cross_benchmark_contrast")
OUTPUT_PATH = OUTPUT_DIR / "q1_cross_benchmark_overall_contrast.csv"
DOC_PATH = Path("docs/occupational_scope/q1_cross_benchmark_contrast_summary.md")


def classify(avg):
    if avg > 0.05:
        return "masculine"
    if avg < -0.05:
        return "feminine"
    return "near-neutral / mixed"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    frames = []

    for benchmark, path in SOURCES:
        if not path.exists():
            print(f"Missing: {path}")
            continue

        df = pd.read_csv(path, encoding="utf-8-sig")
        df["benchmark"] = benchmark

        if "average_score_difference" not in df.columns:
            print(f"Skipped missing average_score_difference: {path}")
            continue

        df["direction"] = df["average_score_difference"].apply(classify)

        keep_cols = [
            "benchmark",
            "model_name",
            "total_items",
            "masculine_preferred_count",
            "feminine_preferred_count",
            "equal_count",
            "masculine_preferred_percent",
            "feminine_preferred_percent",
            "equal_percent",
            "average_score_difference",
            "median_score_difference",
            "direction",
        ]

        keep_cols = [c for c in keep_cols if c in df.columns]
        frames.append(df[keep_cols])

    if not frames:
        raise RuntimeError("No benchmark summaries found.")

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values(["model_name", "benchmark"])
    combined.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# Q1 Cross-Benchmark Contrast Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This document compares model-level gender-preference results across the benchmark suite, "
        "including controlled benchmarks and real-world ArabJobs v7 data."
    )
    doc.append("")
    doc.append("## Output")
    doc.append("")
    doc.append(f"- Combined contrast table: `{OUTPUT_PATH}`")
    doc.append("")
    doc.append("## Cross-Benchmark Direction Changes")
    doc.append("")

    for model, group in combined.groupby("model_name"):
        directions = group["direction"].dropna().unique().tolist()
        doc.append(f"### {model}")
        doc.append("")
        doc.append(f"- Benchmarks covered: {group['benchmark'].nunique()}")
        doc.append(f"- Directions observed: {', '.join(directions)}")
        doc.append(f"- Direction changed across benchmarks: {len(directions) > 1}")
        doc.append("")

        for _, row in group.iterrows():
            doc.append(
                f"  - {row['benchmark']}: avg={row['average_score_difference']}, direction={row['direction']}"
            )
        doc.append("")

    doc.append("## Publication Claim")
    doc.append("")
    doc.append(
        "The cross-benchmark contrast supports the central paper claim that Arabic occupational gender-bias "
        "scores are not fixed model properties. Instead, they vary across benchmark design, template structure, "
        "job-title context, expanded job-role framing, and real-world recruitment-language data."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("Cross-benchmark contrast created.")
    print("CSV:", OUTPUT_PATH)
    print("DOC:", DOC_PATH)
    print("")
    print(combined.to_string(index=False))


if __name__ == "__main__":
    main()