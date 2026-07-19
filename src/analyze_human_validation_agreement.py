from pathlib import Path
import pandas as pd
from sklearn.metrics import cohen_kappa_score


INPUT_PATH = Path("data/human_validation/human_validation_annotation_sheet.csv")
OUTPUT_PATH = Path("results/human_validation/human_validation_agreement_summary.csv")
DOC_PATH = Path("docs/occupational_scope/human_validation_result_summary.md")


FIELDS = [
    "grammaticality",
    "meaning_preserved",
    "gender_form_correct",
    "dialect_correct",
    "keep_or_remove",
]


def percentage_agreement(a, b):
    valid = (a.astype(str).str.strip() != "") & (b.astype(str).str.strip() != "")
    if valid.sum() == 0:
        return None
    return (a[valid].astype(str).str.strip() == b[valid].astype(str).str.strip()).mean()


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Annotation sheet not found: {INPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    rows = []

    for field in FIELDS:
        col1 = f"annotator_1_{field}"
        col2 = f"annotator_2_{field}"

        if col1 not in df.columns or col2 not in df.columns:
            continue

        a = df[col1].fillna("").astype(str).str.strip()
        b = df[col2].fillna("").astype(str).str.strip()

        valid = (a != "") & (b != "")

        if valid.sum() == 0:
            kappa = None
            agreement = None
        else:
            kappa = cohen_kappa_score(a[valid], b[valid])
            agreement = percentage_agreement(a, b)

        rows.append({
            "validation_field": field,
            "annotated_items": int(valid.sum()),
            "percentage_agreement": agreement,
            "cohens_kappa": kappa,
        })

    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    keep_col_1 = "annotator_1_keep_or_remove"
    keep_col_2 = "annotator_2_keep_or_remove"

    total_items = len(df)

    if keep_col_1 in df.columns and keep_col_2 in df.columns:
        keep_both = (
            (df[keep_col_1].fillna("").astype(str).str.strip() == "keep") &
            (df[keep_col_2].fillna("").astype(str).str.strip() == "keep")
        ).sum()
    else:
        keep_both = None

    doc_lines = []
    doc_lines.append("# Human Validation Result Summary")
    doc_lines.append("")
    doc_lines.append("## Purpose")
    doc_lines.append("")
    doc_lines.append("This document reports agreement between two annotators on Arabic benchmark pair quality.")
    doc_lines.append("")
    doc_lines.append("## Summary")
    doc_lines.append("")
    doc_lines.append(f"- Total validation items: {total_items}")
    if keep_both is not None:
        doc_lines.append(f"- Items marked keep by both annotators: {keep_both}")
    doc_lines.append("")
    doc_lines.append("## Agreement Metrics")
    doc_lines.append("")

    for _, row in summary_df.iterrows():
        doc_lines.append(f"### {row['validation_field']}")
        doc_lines.append(f"- Annotated items: {row['annotated_items']}")
        doc_lines.append(f"- Percentage agreement: {row['percentage_agreement']}")
        doc_lines.append(f"- Cohen's Kappa: {row['cohens_kappa']}")
        doc_lines.append("")

    doc_lines.append("## Thesis Use")
    doc_lines.append("")
    doc_lines.append(
        "These results provide a human validation layer for the benchmark suite and support the quality of the Arabic counterfactual sentence pairs."
    )

    DOC_PATH.write_text("\n".join(doc_lines), encoding="utf-8")

    print("Human validation agreement analysis completed.")
    print("Summary:", OUTPUT_PATH)
    print("Document:", DOC_PATH)
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()