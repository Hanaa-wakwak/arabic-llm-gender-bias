from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/external_datasets/job_scraping/scraped_job_title_bias_pairs.csv")
OUTPUT_PATH = Path("data/external_datasets/job_scraping/clean_scraped_job_title_bias_pairs.csv")
REMOVED_PATH = Path("results/external_datasets/job_scraping/removed_scraped_job_title_pairs.csv")
SUMMARY_PATH = Path("results/external_datasets/job_scraping/clean_scraped_job_title_pairs_summary.csv")
SUMMARY_MD = Path("docs/occupational_scope/clean_scraped_job_title_pairs_summary.md")


BAD_CONTEXT_TERMS = [
    "باحث عن عمل",
    "باحثة عن عمل",
    "سجل نفسك",
    "سجل كباحث",
    "تسجيل الدخول",
    "من نحن",
    "تواصل معنا",
]


BAD_OUTPUT_PATTERNS = [
    "مهندسةين",
    "مديرة إداري",
    "مديرة اداري",
]


def detect_issue(row):
    context = str(row.get("original_context_text", ""))
    masculine_sentence = str(row.get("masculine_sentence", ""))
    feminine_sentence = str(row.get("feminine_sentence", ""))

    for term in BAD_CONTEXT_TERMS:
        if term in context:
            return f"non_job_title_context:{term}"

    for pattern in BAD_OUTPUT_PATTERNS:
        if pattern in feminine_sentence or pattern in masculine_sentence:
            return f"invalid_counterfactual_pattern:{pattern}"

    if len(context.strip()) < 4:
        return "too_short_context"

    if masculine_sentence == feminine_sentence:
        return "identical_pair"

    return ""


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REMOVED_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_MD.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    if df.empty:
        raise ValueError("Input file is empty.")

    df["quality_issue"] = df.apply(detect_issue, axis=1)

    clean_df = df[df["quality_issue"] == ""].copy()
    removed_df = df[df["quality_issue"] != ""].copy()

    clean_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    removed_df.to_csv(REMOVED_PATH, index=False, encoding="utf-8-sig")

    summary_df = pd.DataFrame([
        {"metric": "raw_pairs", "value": len(df)},
        {"metric": "clean_pairs", "value": len(clean_df)},
        {"metric": "removed_pairs", "value": len(removed_df)},
        {"metric": "unique_clean_occupations", "value": clean_df["occupation_id"].nunique() if not clean_df.empty else 0},
        {"metric": "unique_clean_fields", "value": clean_df["field"].nunique() if not clean_df.empty else 0},
        {"metric": "manual_review_required", "value": True},
        {"metric": "status", "value": "cleaning_completed"},
    ])

    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Clean Scraped Job-Title Pair Summary")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This step filters the raw scraped job-title counterfactual pairs before scoring."
    )
    md.append("")
    md.append("## Removed Cases")
    md.append("")
    md.append(
        "The cleaner removes non-job-title contexts such as job-seeker registration phrases "
        "and malformed counterfactual replacements such as incorrect plural substitutions."
    )
    md.append("")
    md.append("## Summary")
    md.append("")
    for _, row in summary_df.iterrows():
        md.append(f"- {row['metric']}: {row['value']}")
    md.append("")
    md.append("## Output Files")
    md.append("")
    md.append(f"- Clean pairs: `{OUTPUT_PATH}`")
    md.append(f"- Removed pairs: `{REMOVED_PATH}`")
    md.append(f"- Summary: `{SUMMARY_PATH}`")
    md.append("")
    md.append("## Note")
    md.append("")
    md.append(
        "The cleaned scraped dataset is still an external enrichment pilot and requires manual review."
    )

    SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")

    print("Scraped job-title pair cleaning completed.")
    print("Clean pairs:", OUTPUT_PATH)
    print("Removed pairs:", REMOVED_PATH)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()