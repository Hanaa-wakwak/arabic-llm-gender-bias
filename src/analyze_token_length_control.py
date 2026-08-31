from pathlib import Path
import pandas as pd


INPUTS = [
    ("v6_job_roles", Path("results/occupational_benchmark_v6_job_roles_large_all_models")),
    ("arabjobs_v7", Path("results/external_datasets/arabjobs")),
]

OUTPUT_DIR = Path("results/q1_token_length_control")
DOC_PATH = Path("docs/occupational_scope/q1_token_length_control_summary.md")


def simple_token_count(text):
    if pd.isna(text):
        return 0
    return len(str(text).split())


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    frames = []

    for dataset_name, root in INPUTS:
        if not root.exists():
            continue

        for path in root.glob("scoring_*/*.csv"):
            df = pd.read_csv(path, encoding="utf-8-sig")

            needed = [
                "model_name",
                "masculine_sentence",
                "feminine_sentence",
                "score_difference",
                "preferred_gender",
            ]

            if not all(c in df.columns for c in needed):
                continue

            temp = df.copy()
            temp["dataset_source"] = dataset_name
            temp["masculine_word_count"] = temp["masculine_sentence"].apply(simple_token_count)
            temp["feminine_word_count"] = temp["feminine_sentence"].apply(simple_token_count)
            temp["word_count_difference"] = temp["masculine_word_count"] - temp["feminine_word_count"]
            temp["absolute_word_count_difference"] = temp["word_count_difference"].abs()
            frames.append(temp)

    if not frames:
        raise RuntimeError("No valid scoring outputs found.")

    combined = pd.concat(frames, ignore_index=True)

    combined_path = OUTPUT_DIR / "q1_token_length_control_all_rows.csv"
    combined.to_csv(combined_path, index=False, encoding="utf-8-sig")

    rows = []

    for (dataset, model), group in combined.groupby(["dataset_source", "model_name"]):
        corr = group["score_difference"].astype(float).corr(group["word_count_difference"].astype(float))

        rows.append({
            "dataset_source": dataset,
            "model_name": model,
            "total_items": len(group),
            "mean_masculine_word_count": group["masculine_word_count"].mean(),
            "mean_feminine_word_count": group["feminine_word_count"].mean(),
            "mean_word_count_difference": group["word_count_difference"].mean(),
            "mean_absolute_word_count_difference": group["absolute_word_count_difference"].mean(),
            "correlation_score_difference_with_word_count_difference": corr,
            "same_word_count_percent": (group["absolute_word_count_difference"] == 0).mean() * 100,
        })

    summary = pd.DataFrame(rows)
    summary.to_csv(OUTPUT_DIR / "q1_token_length_control_summary.csv", index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# Q1 Token-Length Control Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This analysis checks whether score_difference is likely to be driven by superficial word-count differences "
        "between masculine and feminine sentence variants."
    )
    doc.append("")
    doc.append("## Method")
    doc.append("")
    doc.append("- Count words in masculine and feminine sentence variants.")
    doc.append("- Compute word_count_difference = masculine_word_count - feminine_word_count.")
    doc.append("- Estimate correlation between word_count_difference and score_difference.")
    doc.append("")
    doc.append("## Output Files")
    doc.append("")
    doc.append(f"- Row-level file: `{combined_path}`")
    doc.append(f"- Summary file: `{OUTPUT_DIR / 'q1_token_length_control_summary.csv'}`")
    doc.append("")
    doc.append("## Summary")
    doc.append("")

    for _, row in summary.iterrows():
        doc.append(f"### {row['dataset_source']} | {row['model_name']}")
        doc.append("")
        doc.append(f"- Total items: {row['total_items']}")
        doc.append(f"- Mean masculine word count: {row['mean_masculine_word_count']}")
        doc.append(f"- Mean feminine word count: {row['mean_feminine_word_count']}")
        doc.append(f"- Mean word-count difference: {row['mean_word_count_difference']}")
        doc.append(f"- Mean absolute word-count difference: {row['mean_absolute_word_count_difference']}")
        doc.append(f"- Same word-count percent: {row['same_word_count_percent']}")
        doc.append(f"- Correlation with score_difference: {row['correlation_score_difference_with_word_count_difference']}")
        doc.append("")

    doc.append("## Publication Claim")
    doc.append("")
    doc.append(
        "This analysis provides a control check showing whether measured gender-preference scores are plausibly explained "
        "by sentence-length differences. Since the main scoring method uses average token log probability, this check adds "
        "an additional surface-form validation layer."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("Token-length control analysis completed.")
    print("Output dir:", OUTPUT_DIR)
    print("Doc:", DOC_PATH)
    print("")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()