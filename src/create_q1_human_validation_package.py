from pathlib import Path
import pandas as pd


DATASETS = [
    {
        "benchmark_name": "v2_main",
        "path": "data/occupational_benchmark/occupational_bias_v2.csv",
        "sample_size": 80,
    },
    {
        "benchmark_name": "v4_template_perturbation",
        "path": "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv",
        "sample_size": 100,
    },
    {
        "benchmark_name": "v5_job_titles",
        "path": "data/occupational_benchmark/occupational_bias_v5_job_titles.csv",
        "sample_size": 80,
    },
    {
        "benchmark_name": "v6_job_roles_departments",
        "path": "data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv",
        "sample_size": 140,
    },
    {
        "benchmark_name": "arabjobs_v7_external",
        "path": "data/external_datasets/arabjobs/arabjobs_v7_counterfactual_pairs.csv",
        "sample_size": 100,
    },
]

OUTPUT_DIR = Path("data/human_validation/q1_validation")
RESULTS_DIR = Path("results/human_validation/q1_validation")
DOC_DIR = Path("docs/occupational_scope")

FULL_SHEET = OUTPUT_DIR / "q1_human_validation_annotation_sheet.csv"
ANNOTATOR_1_SHEET = OUTPUT_DIR / "q1_human_validation_annotator_1.csv"
ANNOTATOR_2_SHEET = OUTPUT_DIR / "q1_human_validation_annotator_2.csv"
SAMPLING_SUMMARY = RESULTS_DIR / "q1_human_validation_sampling_summary.csv"
PROTOCOL_DOC = DOC_DIR / "q1_human_validation_protocol.md"


def normalize_columns(df):
    df = df.copy()

    column_defaults = {
        "id": "",
        "benchmark_version": "",
        "field": "",
        "department": "",
        "occupation_key": "",
        "role_key": "",
        "job_family": "",
        "seniority_level": "",
        "job_role_type": "",
        "workplace_context": "",
        "country": "",
        "job_category": "",
        "sub_category": "",
        "profession": "",
        "original_gender_label": "",
        "original_job_title": "",
        "masculine_occupation": "",
        "feminine_occupation": "",
        "masculine_job_title": "",
        "feminine_job_title": "",
        "template_id": "",
        "template_type": "",
        "semantic_frame": "",
        "dialect": "",
        "masculine_sentence": "",
        "feminine_sentence": "",
        "stereotype_label": "",
    }

    for col, default in column_defaults.items():
        if col not in df.columns:
            df[col] = default

    if "department" in df.columns and "field" in df.columns:
        df["field"] = df["field"].fillna("")
        df.loc[df["field"].astype(str).str.strip() == "", "field"] = df["department"]

    if "role_key" in df.columns and "occupation_key" in df.columns:
        df["occupation_key"] = df["occupation_key"].fillna("")
        df.loc[df["occupation_key"].astype(str).str.strip() == "", "occupation_key"] = df["role_key"]

    if "masculine_job_title" in df.columns and "masculine_occupation" in df.columns:
        df["masculine_job_title"] = df["masculine_job_title"].fillna("")
        df.loc[df["masculine_job_title"].astype(str).str.strip() == "", "masculine_job_title"] = df["masculine_occupation"]

    if "feminine_job_title" in df.columns and "feminine_occupation" in df.columns:
        df["feminine_job_title"] = df["feminine_job_title"].fillna("")
        df.loc[df["feminine_job_title"].astype(str).str.strip() == "", "feminine_job_title"] = df["feminine_occupation"]

    return df


def stratified_sample(df, sample_size, benchmark_name):
    df = df.copy()

    stratify_cols = []
    for col in ["dialect", "template_type", "field", "department"]:
        if col in df.columns and df[col].nunique(dropna=True) > 1:
            stratify_cols.append(col)

    if not stratify_cols:
        sample_n = min(sample_size, len(df))
        return df.sample(n=sample_n, random_state=42)

    df["_stratum"] = df[stratify_cols].astype(str).agg("|".join, axis=1)
    strata = df["_stratum"].dropna().unique().tolist()

    sampled_parts = []
    per_stratum = max(1, sample_size // max(1, len(strata)))

    for stratum, group in df.groupby("_stratum"):
        n = min(per_stratum, len(group))
        sampled_parts.append(group.sample(n=n, random_state=42))

    sampled = pd.concat(sampled_parts, ignore_index=True)

    if len(sampled) < sample_size:
        remaining = df.drop(sampled.index, errors="ignore")
        if not remaining.empty:
            extra_n = min(sample_size - len(sampled), len(remaining))
            sampled = pd.concat(
                [sampled, remaining.sample(n=extra_n, random_state=43)],
                ignore_index=True,
            )

    if len(sampled) > sample_size:
        sampled = sampled.sample(n=sample_size, random_state=44)

    sampled = sampled.drop(columns=["_stratum"], errors="ignore")
    return sampled


def make_annotator_sheet(df, annotator_id):
    sheet = df.copy()

    sheet[f"annotator_{annotator_id}_grammaticality"] = ""
    sheet[f"annotator_{annotator_id}_meaning_preserved"] = ""
    sheet[f"annotator_{annotator_id}_gender_form_correct"] = ""
    sheet[f"annotator_{annotator_id}_dialect_correct"] = ""
    sheet[f"annotator_{annotator_id}_job_title_correct"] = ""
    sheet[f"annotator_{annotator_id}_keep_or_remove"] = ""
    sheet[f"annotator_{annotator_id}_notes"] = ""

    return sheet


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)

    all_samples = []
    summary_rows = []

    for dataset in DATASETS:
        benchmark_name = dataset["benchmark_name"]
        path = Path(dataset["path"])
        sample_size = dataset["sample_size"]

        if not path.exists():
            summary_rows.append({
                "benchmark_name": benchmark_name,
                "input_file": str(path),
                "available_rows": 0,
                "sampled_rows": 0,
                "status": "missing_file",
            })
            continue

        df = pd.read_csv(path, encoding="utf-8-sig")
        df = normalize_columns(df)

        sample_n = min(sample_size, len(df))
        sampled = stratified_sample(df, sample_n, benchmark_name)

        sampled["validation_source_benchmark"] = benchmark_name
        sampled["validation_input_file"] = str(path)

        all_samples.append(sampled)

        summary_rows.append({
            "benchmark_name": benchmark_name,
            "input_file": str(path),
            "available_rows": len(df),
            "sampled_rows": len(sampled),
            "status": "sampled",
        })

    if not all_samples:
        raise RuntimeError("No validation samples were created.")

    combined = pd.concat(all_samples, ignore_index=True)

    combined.insert(
        0,
        "validation_id",
        [f"Q1HV_{i + 1:04d}" for i in range(len(combined))]
    )

    keep_cols = [
        "validation_id",
        "validation_source_benchmark",
        "validation_input_file",
        "id",
        "benchmark_version",
        "field",
        "department",
        "occupation_key",
        "role_key",
        "job_family",
        "seniority_level",
        "job_role_type",
        "workplace_context",
        "country",
        "job_category",
        "sub_category",
        "profession",
        "original_gender_label",
        "original_job_title",
        "stereotype_label",
        "masculine_occupation",
        "feminine_occupation",
        "masculine_job_title",
        "feminine_job_title",
        "template_id",
        "template_type",
        "semantic_frame",
        "dialect",
        "masculine_sentence",
        "feminine_sentence",
    ]

    keep_cols = [c for c in keep_cols if c in combined.columns]
    combined = combined[keep_cols]

    full_sheet = combined.copy()

    for annotator_id in [1, 2]:
        full_sheet[f"annotator_{annotator_id}_grammaticality"] = ""
        full_sheet[f"annotator_{annotator_id}_meaning_preserved"] = ""
        full_sheet[f"annotator_{annotator_id}_gender_form_correct"] = ""
        full_sheet[f"annotator_{annotator_id}_dialect_correct"] = ""
        full_sheet[f"annotator_{annotator_id}_job_title_correct"] = ""
        full_sheet[f"annotator_{annotator_id}_keep_or_remove"] = ""
        full_sheet[f"annotator_{annotator_id}_notes"] = ""

    full_sheet.to_csv(FULL_SHEET, index=False, encoding="utf-8-sig")

    annotator_1 = make_annotator_sheet(combined, 1)
    annotator_2 = make_annotator_sheet(combined, 2)

    annotator_1.to_csv(ANNOTATOR_1_SHEET, index=False, encoding="utf-8-sig")
    annotator_2.to_csv(ANNOTATOR_2_SHEET, index=False, encoding="utf-8-sig")

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(SAMPLING_SUMMARY, index=False, encoding="utf-8-sig")

    protocol = []
    protocol.append("# Q1 Human Validation Protocol")
    protocol.append("")
    protocol.append("## Purpose")
    protocol.append("")
    protocol.append(
        "This protocol validates a stratified sample of Arabic masculine-feminine occupational counterfactual pairs "
        "from controlled benchmarks and external real-world job-ad data."
    )
    protocol.append("")
    protocol.append("## Validation Sources")
    protocol.append("")
    protocol.append("- v2 main occupational benchmark")
    protocol.append("- v4 template perturbation benchmark")
    protocol.append("- v5 job-title benchmark")
    protocol.append("- v6 expanded job-role and department benchmark")
    protocol.append("- ArabJobs v7 external real-world job-ad benchmark")
    protocol.append("")
    protocol.append("## Target Sample")
    protocol.append("")
    protocol.append(f"- Total validation pairs: {len(full_sheet)}")
    protocol.append("- Annotators: 2")
    protocol.append("")
    protocol.append("## Annotation Labels")
    protocol.append("")
    protocol.append("### grammaticality")
    protocol.append("- valid")
    protocol.append("- minor_issue")
    protocol.append("- invalid")
    protocol.append("")
    protocol.append("### meaning_preserved")
    protocol.append("- yes")
    protocol.append("- mostly")
    protocol.append("- no")
    protocol.append("")
    protocol.append("### gender_form_correct")
    protocol.append("- yes")
    protocol.append("- no")
    protocol.append("")
    protocol.append("### dialect_correct")
    protocol.append("- yes")
    protocol.append("- no")
    protocol.append("- uncertain")
    protocol.append("")
    protocol.append("### job_title_correct")
    protocol.append("- yes")
    protocol.append("- no")
    protocol.append("- uncertain")
    protocol.append("")
    protocol.append("### keep_or_remove")
    protocol.append("- keep")
    protocol.append("- review")
    protocol.append("- remove")
    protocol.append("")
    protocol.append("## Agreement Metrics")
    protocol.append("")
    protocol.append("After annotation, the project reports:")
    protocol.append("")
    protocol.append("- percentage agreement")
    protocol.append("- Cohen's Kappa")
    protocol.append("- valid-pair rate")
    protocol.append("- keep/review/remove distribution")
    protocol.append("")
    protocol.append("## Q1 Publication Value")
    protocol.append("")
    protocol.append(
        "This validation layer strengthens benchmark reliability by showing that Arabic counterfactual pairs were manually reviewed "
        "for grammaticality, meaning preservation, gender-form correctness, dialect appropriateness, and job-title validity."
    )

    PROTOCOL_DOC.write_text("\n".join(protocol), encoding="utf-8")

    print("Q1 human validation package created.")
    print("Full sheet:", FULL_SHEET)
    print("Annotator 1 sheet:", ANNOTATOR_1_SHEET)
    print("Annotator 2 sheet:", ANNOTATOR_2_SHEET)
    print("Sampling summary:", SAMPLING_SUMMARY)
    print("Protocol:", PROTOCOL_DOC)
    print("")
    print(summary_df.to_string(index=False))
    print("")
    print("Total validation pairs:", len(full_sheet))


if __name__ == "__main__":
    main()