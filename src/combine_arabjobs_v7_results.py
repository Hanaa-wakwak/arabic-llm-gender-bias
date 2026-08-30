from pathlib import Path
import pandas as pd


BASE_DIR = Path("results/external_datasets/arabjobs")
OUTPUT_DIR = BASE_DIR / "combined_analysis"
OUTPUT_PATH = OUTPUT_DIR / "arabjobs_v7_overall_by_model.csv"
DOC_PATH = Path("docs/occupational_scope/arabjobs_v7_model_result_summary.md")


def classify_direction(avg_score):
    if avg_score > 0.05:
        return "masculine"
    if avg_score < -0.05:
        return "feminine"
    return "near-neutral / mixed"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    summary_files = list(BASE_DIR.glob("analysis_*/summary_overall.csv"))

    if not summary_files:
        raise RuntimeError("No ArabJobs summary_overall.csv files found.")

    frames = []

    for path in summary_files:
        df = pd.read_csv(path, encoding="utf-8-sig")
        df["source_file"] = str(path)
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    combined["arabjobs_v7_direction"] = combined["average_score_difference"].apply(classify_direction)
    combined = combined.sort_values("model_name")

    combined.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# ArabJobs v7 Model Result Summary")
    doc.append("")
    doc.append("## Dataset")
    doc.append("")
    doc.append("- Dataset: ArabJobs v7 external real-world Arabic job-ad benchmark")
    doc.append("- Source: ArabJobs: A Multinational Corpus of Arabic Job Ads")
    doc.append("- Evaluation type: external real-world recruitment-language validation")
    doc.append("- Counterfactual pairs are generated from matched ArabJobs job-title contexts")
    doc.append("")
    doc.append("## Overall Results")
    doc.append("")

    for _, row in combined.iterrows():
        doc.append(f"### {row['model_name']}")
        doc.append("")
        doc.append(f"- Total items: {row['total_items']}")
        doc.append(f"- Masculine preferred: {row['masculine_preferred_count']} ({row['masculine_preferred_percent']}%)")
        doc.append(f"- Feminine preferred: {row['feminine_preferred_count']} ({row['feminine_preferred_percent']}%)")
        doc.append(f"- Equal: {row['equal_count']} ({row['equal_percent']}%)")
        doc.append(f"- Average score difference: {row['average_score_difference']}")
        doc.append(f"- Median score difference: {row['median_score_difference']}")
        doc.append(f"- Direction: {row['arabjobs_v7_direction']}")
        doc.append("")

    doc.append("## Interpretation")
    doc.append("")
    doc.append(
        "ArabJobs v7 extends the thesis beyond controlled benchmark construction by evaluating "
        "the same paired-likelihood scoring method on real-world Arabic recruitment-language data. "
        "This allows comparison between controlled job-role benchmarks and naturally occurring job-ad contexts."
    )
    doc.append("")
    doc.append("## Thesis Value")
    doc.append("")
    doc.append(
        "This external dataset strengthens the Q1-readiness of the work by adding real-world validation "
        "from Arabic job advertisements and showing whether measured gender preference remains stable "
        "outside synthetic templates."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("ArabJobs combined result summary created.")
    print("CSV:", OUTPUT_PATH)
    print("DOC:", DOC_PATH)
    print("")
    print(combined.to_string(index=False))


if __name__ == "__main__":
    main()