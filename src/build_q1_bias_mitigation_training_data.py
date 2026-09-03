from pathlib import Path
import pandas as pd


INPUTS = [
    Path("data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv"),
    Path("data/occupational_benchmark/occupational_bias_v5_job_titles.csv"),
]

OUTPUT_DIR = Path("data/q1_bias_mitigation")
TRAIN_TXT = OUTPUT_DIR / "arabic_counterfactual_mitigation_train.txt"
TRAIN_CSV = OUTPUT_DIR / "arabic_counterfactual_mitigation_train.csv"
SUMMARY_CSV = OUTPUT_DIR / "arabic_counterfactual_mitigation_training_summary.csv"
DOC_PATH = Path("docs/occupational_scope/q1_bias_mitigation_training_data_summary.md")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    summary = []

    for path in INPUTS:
        if not path.exists():
            summary.append({
                "input_file": str(path),
                "status": "missing",
                "pairs_loaded": 0,
                "training_sentences_created": 0,
            })
            continue

        df = pd.read_csv(path, encoding="utf-8-sig")

        required = ["masculine_sentence", "feminine_sentence"]
        missing = [c for c in required if c not in df.columns]

        if missing:
            summary.append({
                "input_file": str(path),
                "status": "missing_columns",
                "missing_columns": ",".join(missing),
                "pairs_loaded": 0,
                "training_sentences_created": 0,
            })
            continue

        for idx, row in df.iterrows():
            base = {
                "source_file": str(path),
                "source_row": idx,
                "template_id": row.get("template_id", ""),
                "dialect": row.get("dialect", ""),
                "field": row.get("field", row.get("department", "")),
                "department": row.get("department", ""),
                "job_family": row.get("job_family", ""),
                "semantic_frame": row.get("semantic_frame", ""),
            }

            rows.append({
                **base,
                "gender_variant": "masculine",
                "text": str(row["masculine_sentence"]).strip(),
            })

            rows.append({
                **base,
                "gender_variant": "feminine",
                "text": str(row["feminine_sentence"]).strip(),
            })

        summary.append({
            "input_file": str(path),
            "status": "loaded",
            "pairs_loaded": len(df),
            "training_sentences_created": len(df) * 2,
        })

    train_df = pd.DataFrame(rows)

    train_df = train_df.dropna(subset=["text"])
    train_df = train_df[train_df["text"].astype(str).str.strip() != ""]

    # Balance masculine and feminine exactly.
    masculine_df = train_df[train_df["gender_variant"] == "masculine"]
    feminine_df = train_df[train_df["gender_variant"] == "feminine"]

    n = min(len(masculine_df), len(feminine_df))

    balanced_df = pd.concat(
        [
            masculine_df.sample(n=n, random_state=42),
            feminine_df.sample(n=n, random_state=42),
        ],
        ignore_index=True,
    ).sample(frac=1, random_state=43)

    balanced_df.to_csv(TRAIN_CSV, index=False, encoding="utf-8-sig")

    TRAIN_TXT.write_text(
        "\n".join(balanced_df["text"].astype(str).tolist()),
        encoding="utf-8",
    )

    summary_df = pd.DataFrame(summary)
    summary_df.loc[len(summary_df)] = {
        "input_file": "TOTAL_BALANCED",
        "status": "created",
        "pairs_loaded": "",
        "training_sentences_created": len(balanced_df),
    }

    summary_df.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# Q1 Bias Mitigation Training Data Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This file documents the construction of balanced Arabic masculine-feminine counterfactual training data "
        "for the Q1 bias mitigation experiment."
    )
    doc.append("")
    doc.append("## Method")
    doc.append("")
    doc.append("- Load controlled Arabic occupational counterfactual pairs.")
    doc.append("- Extract both masculine and feminine sentence variants.")
    doc.append("- Balance masculine and feminine variants exactly.")
    doc.append("- Export a text corpus for causal language model fine-tuning.")
    doc.append("")
    doc.append("## Output Files")
    doc.append("")
    doc.append(f"- Training CSV: `{TRAIN_CSV}`")
    doc.append(f"- Training TXT: `{TRAIN_TXT}`")
    doc.append(f"- Summary CSV: `{SUMMARY_CSV}`")
    doc.append("")
    doc.append("## Training Sentences")
    doc.append("")
    doc.append(f"- Total balanced training sentences: {len(balanced_df)}")
    doc.append(f"- Masculine sentences: {int((balanced_df['gender_variant'] == 'masculine').sum())}")
    doc.append(f"- Feminine sentences: {int((balanced_df['gender_variant'] == 'feminine').sum())}")
    doc.append("")
    doc.append("## Publication Value")
    doc.append("")
    doc.append(
        "This dataset supports a counterfactual data augmentation mitigation experiment, testing whether exposure to balanced "
        "Arabic masculine-feminine occupational contexts reduces measured gender preference."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("Mitigation training data created.")
    print("Training CSV:", TRAIN_CSV)
    print("Training TXT:", TRAIN_TXT)
    print("Summary:", SUMMARY_CSV)
    print("Doc:", DOC_PATH)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()