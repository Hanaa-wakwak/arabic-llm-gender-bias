from pathlib import Path
import pandas as pd
from sklearn.metrics import cohen_kappa_score


ANNOTATOR_1_PATH = Path("data/human_validation/q1_validation/q1_human_validation_annotator_1.csv")
ANNOTATOR_2_PATH = Path("data/human_validation/q1_validation/q1_human_validation_annotator_2.csv")

OUTPUT_DIR = Path("results/human_validation/q1_validation")
MERGED_OUTPUT = OUTPUT_DIR / "q1_human_validation_merged_annotations.csv"
AGREEMENT_OUTPUT = OUTPUT_DIR / "q1_human_validation_agreement_summary.csv"
BENCHMARK_OUTPUT = OUTPUT_DIR / "q1_human_validation_by_benchmark_summary.csv"
DOC_PATH = Path("docs/occupational_scope/q1_human_validation_result_summary.md")


FIELDS = [
    "grammaticality",
    "meaning_preserved",
    "gender_form_correct",
    "dialect_correct",
    "job_title_correct",
    "keep_or_remove",
]


def clean_series(series):
    return series.fillna("").astype(str).str.strip().str.lower()


def percent_agreement(a, b):
    valid = (a != "") & (b != "")
    if valid.sum() == 0:
        return None
    return float((a[valid] == b[valid]).mean())


def safe_kappa(a, b):
    valid = (a != "") & (b != "")
    if valid.sum() == 0:
        return None
    if a[valid].nunique() == 1 and b[valid].nunique() == 1:
        return 1.0 if (a[valid].iloc[0] == b[valid].iloc[0]) else 0.0
    return float(cohen_kappa_score(a[valid], b[valid]))


def main():
    if not ANNOTATOR_1_PATH.exists():
        raise FileNotFoundError(f"Missing annotator 1 file: {ANNOTATOR_1_PATH}")
    if not ANNOTATOR_2_PATH.exists():
        raise FileNotFoundError(f"Missing annotator 2 file: {ANNOTATOR_2_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    a1 = pd.read_csv(ANNOTATOR_1_PATH, encoding="utf-8-sig")
    a2 = pd.read_csv(ANNOTATOR_2_PATH, encoding="utf-8-sig")

    if "validation_id" not in a1.columns or "validation_id" not in a2.columns:
        raise ValueError("Both annotation sheets must contain validation_id.")

    base_cols = [
        "validation_id",
        "validation_source_benchmark",
        "id",
        "field",
        "department",
        "occupation_key",
        "role_key",
        "masculine_occupation",
        "feminine_occupation",
        "template_id",
        "template_type",
        "semantic_frame",
        "dialect",
        "masculine_sentence",
        "feminine_sentence",
    ]
    base_cols = [c for c in base_cols if c in a1.columns]

    annotator_1_cols = ["validation_id"] + [f"annotator_1_{field}" for field in FIELDS] + ["annotator_1_notes"]
    annotator_2_cols = ["validation_id"] + [f"annotator_2_{field}" for field in FIELDS] + ["annotator_2_notes"]

    annotator_1_cols = [c for c in annotator_1_cols if c in a1.columns]
    annotator_2_cols = [c for c in annotator_2_cols if c in a2.columns]

    merged = a1[base_cols + [c for c in annotator_1_cols if c != "validation_id"]].merge(
        a2[annotator_2_cols],
        on="validation_id",
        how="left",
    )

    merged.to_csv(MERGED_OUTPUT, index=False, encoding="utf-8-sig")

    agreement_rows = []

    for field in FIELDS:
        c1 = f"annotator_1_{field}"
        c2 = f"annotator_2_{field}"

        if c1 not in merged.columns or c2 not in merged.columns:
            continue

        s1 = clean_series(merged[c1])
        s2 = clean_series(merged[c2])
        valid = (s1 != "") & (s2 != "")

        agreement_rows.append({
            "validation_field": field,
            "annotated_items": int(valid.sum()),
            "percentage_agreement": percent_agreement(s1, s2),
            "cohens_kappa": safe_kappa(s1, s2),
            "annotator_1_unique_labels": ",".join(sorted(s1[valid].unique())) if valid.sum() else "",
            "annotator_2_unique_labels": ",".join(sorted(s2[valid].unique())) if valid.sum() else "",
        })

    agreement_df = pd.DataFrame(agreement_rows)
    agreement_df.to_csv(AGREEMENT_OUTPUT, index=False, encoding="utf-8-sig")

    benchmark_rows = []

    if "validation_source_benchmark" in merged.columns:
        for benchmark, group in merged.groupby("validation_source_benchmark"):
            total = len(group)

            keep_1 = clean_series(group.get("annotator_1_keep_or_remove", pd.Series([""] * total)))
            keep_2 = clean_series(group.get("annotator_2_keep_or_remove", pd.Series([""] * total)))

            both_keep = ((keep_1 == "keep") & (keep_2 == "keep")).sum()
            any_remove = ((keep_1 == "remove") | (keep_2 == "remove")).sum()
            any_review = ((keep_1 == "review") | (keep_2 == "review")).sum()

            benchmark_rows.append({
                "validation_source_benchmark": benchmark,
                "total_items": total,
                "both_annotators_keep": int(both_keep),
                "any_annotator_review": int(any_review),
                "any_annotator_remove": int(any_remove),
                "both_keep_percent": float((both_keep / total) * 100) if total else 0,
            })

    benchmark_df = pd.DataFrame(benchmark_rows)
    benchmark_df.to_csv(BENCHMARK_OUTPUT, index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# Q1 Human Validation Result Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This document reports human validation and inter-annotator agreement for the Arabic occupational gender-bias benchmark suite."
    )
    doc.append("")
    doc.append("## Files")
    doc.append("")
    doc.append(f"- Merged annotations: `{MERGED_OUTPUT}`")
    doc.append(f"- Agreement summary: `{AGREEMENT_OUTPUT}`")
    doc.append(f"- Benchmark summary: `{BENCHMARK_OUTPUT}`")
    doc.append("")
    doc.append("## Agreement Metrics")
    doc.append("")

    for _, row in agreement_df.iterrows():
        doc.append(f"### {row['validation_field']}")
        doc.append("")
        doc.append(f"- Annotated items: {row['annotated_items']}")
        doc.append(f"- Percentage agreement: {row['percentage_agreement']}")
        doc.append(f"- Cohen's Kappa: {row['cohens_kappa']}")
        doc.append("")

    doc.append("## Benchmark-Level Validity")
    doc.append("")

    for _, row in benchmark_df.iterrows():
        doc.append(f"### {row['validation_source_benchmark']}")
        doc.append("")
        doc.append(f"- Total items: {row['total_items']}")
        doc.append(f"- Both annotators keep: {row['both_annotators_keep']}")
        doc.append(f"- Any annotator review: {row['any_annotator_review']}")
        doc.append(f"- Any annotator remove: {row['any_annotator_remove']}")
        doc.append(f"- Both-keep percent: {row['both_keep_percent']}")
        doc.append("")

    doc.append("## Thesis and Publication Use")
    doc.append("")
    doc.append(
        "This validation strengthens the reliability of the benchmark by providing human evidence for grammaticality, "
        "meaning preservation, gender-form correctness, dialect appropriateness, job-title correctness, and keep/remove decisions."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("Q1 human validation analysis completed.")
    print("Merged:", MERGED_OUTPUT)
    print("Agreement:", AGREEMENT_OUTPUT)
    print("Benchmark summary:", BENCHMARK_OUTPUT)
    print("Doc:", DOC_PATH)
    print("")
    print(agreement_df.to_string(index=False))
    print("")
    print(benchmark_df.to_string(index=False))


if __name__ == "__main__":
    main()