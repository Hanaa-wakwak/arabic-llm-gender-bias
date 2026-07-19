from pathlib import Path
import pandas as pd


INPUT_FILES = [
    ("v2_main", "data/occupational_benchmark/occupational_bias_v2.csv", 60),
    ("v4_template_perturbation", "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv", 80),
    ("v5_job_titles", "data/occupational_benchmark/occupational_bias_v5_job_titles.csv", 60),
]

OUTPUT_PATH = Path("data/human_validation/human_validation_annotation_sheet.csv")
SUMMARY_PATH = Path("results/human_validation/human_validation_sampling_summary.csv")
DOC_PATH = Path("docs/occupational_scope/human_validation_protocol.md")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    sampled_frames = []
    summary_rows = []

    for benchmark_name, path, n_sample in INPUT_FILES:
        file_path = Path(path)

        if not file_path.exists():
            print(f"Skipped missing file: {file_path}")
            continue

        df = pd.read_csv(file_path, encoding="utf-8-sig")
        df = df.copy()
        df["benchmark_name"] = benchmark_name

        sample_n = min(n_sample, len(df))
        sampled = df.sample(n=sample_n, random_state=42).copy()

        sampled_frames.append(sampled)

        summary_rows.append({
            "benchmark_name": benchmark_name,
            "input_file": path,
            "available_rows": len(df),
            "sampled_rows": sample_n,
        })

    if not sampled_frames:
        raise RuntimeError("No benchmark input files found.")

    annotation_df = pd.concat(sampled_frames, ignore_index=True)
    annotation_df.insert(
        0,
        "validation_id",
        [f"HV_{i + 1:04d}" for i in range(len(annotation_df))]
    )

    keep_cols = [
        "validation_id",
        "benchmark_name",
        "id",
        "occupation_id",
        "field",
        "occupation_key",
        "masculine_occupation",
        "feminine_occupation",
        "stereotype_label",
        "dialect",
        "template_id",
        "template_type",
        "semantic_frame",
        "masculine_sentence",
        "feminine_sentence",
    ]

    keep_cols = [col for col in keep_cols if col in annotation_df.columns]
    annotation_df = annotation_df[keep_cols]

    # Annotator 1 fields
    annotation_df["annotator_1_grammaticality"] = ""
    annotation_df["annotator_1_meaning_preserved"] = ""
    annotation_df["annotator_1_gender_form_correct"] = ""
    annotation_df["annotator_1_dialect_correct"] = ""
    annotation_df["annotator_1_keep_or_remove"] = ""
    annotation_df["annotator_1_notes"] = ""

    # Annotator 2 fields
    annotation_df["annotator_2_grammaticality"] = ""
    annotation_df["annotator_2_meaning_preserved"] = ""
    annotation_df["annotator_2_gender_form_correct"] = ""
    annotation_df["annotator_2_dialect_correct"] = ""
    annotation_df["annotator_2_keep_or_remove"] = ""
    annotation_df["annotator_2_notes"] = ""

    annotation_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    protocol = """# Human Validation Protocol

## Purpose

This protocol validates a sample of Arabic masculine-feminine occupational counterfactual pairs used in the benchmark suite.

The validation checks whether the benchmark pairs are grammatically acceptable, meaning-preserving, gender-form correct, and dialect-appropriate.

## Validation Sample

The annotation sheet samples items from:

- v2 main benchmark
- v4 template perturbation benchmark
- v5 job-title benchmark

## Annotator Instructions

Each annotator should review the masculine and feminine sentence pair and fill the following fields.

### 1. grammaticality

Allowed labels:

- valid
- minor_issue
- invalid

Question:

Are both Arabic sentences grammatically acceptable?

### 2. meaning_preserved

Allowed labels:

- yes
- mostly
- no

Question:

Does the feminine sentence preserve the same meaning as the masculine sentence except for gendered occupation form?

### 3. gender_form_correct

Allowed labels:

- yes
- no

Question:

Are the masculine and feminine occupational forms correct?

### 4. dialect_correct

Allowed labels:

- yes
- no
- uncertain

Question:

Does the sentence match the intended Arabic variety or dialect?

### 5. keep_or_remove

Allowed labels:

- keep
- review
- remove

Question:

Should this pair be kept in the benchmark?

## Agreement Analysis

After annotation, the project will compute:

- percentage agreement
- Cohen's Kappa

## Thesis Use

The validation result will be used as a quality-control layer for the benchmark suite.

This strengthens the thesis by showing that the Arabic counterfactual pairs were reviewed for grammaticality, meaning preservation, gender-form correctness, and dialect appropriateness.
"""

    DOC_PATH.write_text(protocol, encoding="utf-8")

    print("Human validation sheet created.")
    print("Annotation sheet:", OUTPUT_PATH)
    print("Summary:", SUMMARY_PATH)
    print("Protocol:", DOC_PATH)
    print("")
    print(summary_df.to_string(index=False))
    print("")
    print("Total annotation items:", len(annotation_df))


if __name__ == "__main__":
    main()