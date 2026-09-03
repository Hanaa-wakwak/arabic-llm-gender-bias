from pathlib import Path
import subprocess
import py_compile
import pandas as pd


ROOT = Path(".")
OUTPUT_DIR = Path("results/final_q1_audit")
DOC_DIR = Path("docs/occupational_scope")

AUDIT_CSV = OUTPUT_DIR / "full_q1_project_audit_report.csv"
AUDIT_MD = DOC_DIR / "full_q1_project_audit_summary.md"


EXPECTED_DATASETS = [
    {
        "name": "v2_main_benchmark",
        "path": "data/occupational_benchmark/occupational_bias_v2.csv",
        "expected_rows": 240,
        "required_columns": ["masculine_sentence", "feminine_sentence", "template_id", "dialect"],
    },
    {
        "name": "v4_template_perturbation",
        "path": "data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv",
        "expected_rows": 720,
        "required_columns": ["masculine_sentence", "feminine_sentence", "template_id", "semantic_frame", "dialect"],
    },
    {
        "name": "v5_job_titles",
        "path": "data/occupational_benchmark/occupational_bias_v5_job_titles.csv",
        "expected_rows": 540,
        "required_columns": ["masculine_sentence", "feminine_sentence", "template_id", "template_type", "dialect"],
    },
    {
        "name": "v6_job_roles_departments",
        "path": "data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv",
        "expected_rows": 2880,
        "required_columns": [
            "masculine_sentence",
            "feminine_sentence",
            "template_id",
            "template_type",
            "semantic_frame",
            "dialect",
            "department",
            "field",
            "job_family",
            "job_role_type",
        ],
    },
    {
        "name": "arabjobs_v7_external",
        "path": "data/external_datasets/arabjobs/arabjobs_v7_counterfactual_pairs.csv",
        "expected_rows": 14532,
        "required_columns": ["masculine_sentence", "feminine_sentence", "template_id", "country"],
    },
    {
        "name": "q1_mitigation_training_data",
        "path": "data/q1_bias_mitigation/arabic_counterfactual_mitigation_train.csv",
        "expected_rows": None,
        "required_columns": ["gender_variant", "text"],
    },
    {
        "name": "q1_human_validation_sheet",
        "path": "data/human_validation/q1_validation/q1_human_validation_annotation_sheet.csv",
        "expected_rows": 500,
        "required_columns": ["validation_id", "masculine_sentence", "feminine_sentence"],
    },
]


EXPECTED_RESULT_FILES = [
    "results/final_package/score_difference_validation_report.csv",
    "results/q1_formula_validation/q1_formula_validation_report.csv",
    "results/q1_formula_validation/q1_formula_aggregate_validation.csv",
    "results/q1_statistical_modeling/q1_factor_effect_strength_summary.csv",
    "results/q1_cross_benchmark_contrast/q1_cross_benchmark_overall_contrast.csv",
    "results/q1_token_length_control/q1_token_length_control_summary.csv",
    "results/q1_bias_mitigation/q1_bias_mitigation_effect_summary.csv",
    "results/human_validation/q1_validation/q1_human_validation_sampling_summary.csv",
]


EXPECTED_DOCS = [
    "docs/occupational_scope/final_formula_framework_for_q1.md",
    "docs/occupational_scope/q1_formula_validation_summary.md",
    "docs/occupational_scope/q1_statistical_modeling_summary.md",
    "docs/occupational_scope/q1_cross_benchmark_contrast_summary.md",
    "docs/occupational_scope/q1_token_length_control_summary.md",
    "docs/occupational_scope/q1_bias_mitigation_training_data_summary.md",
    "docs/occupational_scope/q1_bias_mitigation_effect_summary.md",
    "docs/occupational_scope/q1_human_validation_protocol.md",
    "docs/occupational_scope/v6_job_roles_benchmark_summary.md",
    "docs/occupational_scope/v6_large_all_models_result_summary.md",
    "docs/occupational_scope/arabjobs_v7_external_dataset_summary.md",
    "docs/occupational_scope/arabjobs_v7_model_result_summary.md",
]


EXPECTED_SOFTWARE_FILES = [
    "software_bias_measurement/app.py",
    "software_bias_measurement/requirements.txt",
    "software_bias_measurement/README.md",
    "software_bias_measurement/run_bias_measurement_app.ps1",
    "software_bias_measurement/run_bias_measurement_app.bat",
    "software_dashboard/app.py",
    "software_dashboard/requirements.txt",
    "software_dashboard/README.md",
    "software_dashboard/run_dashboard_app.ps1",
    "software_dashboard/run_dashboard_app.bat",
    "RUN_SOFTWARE.md",
]


EXPECTED_SCRIPTS = [
    "src/score_occupational_single_model_v1.py",
    "src/analyze_occupational_results_v1.py",
    "src/build_job_roles_expanded_lexicon_v6.py",
    "src/build_occupational_benchmark_v6_job_roles_departments.py",
    "src/check_v6_job_roles_quality.py",
    "src/combine_v6_large_model_results.py",
    "src/prepare_arabjobs_external_dataset_v7.py",
    "src/combine_arabjobs_v7_results.py",
    "src/create_q1_human_validation_package.py",
    "src/analyze_q1_human_validation_agreement.py",
    "src/validate_score_difference_outputs.py",
    "src/validate_formula_framework_q1.py",
    "src/run_q1_statistical_modeling.py",
    "src/create_cross_benchmark_q1_contrast.py",
    "src/analyze_token_length_control.py",
    "src/build_q1_bias_mitigation_training_data.py",
    "src/finetune_q1_counterfactual_mitigation.py",
    "src/analyze_q1_bias_mitigation_effect.py",
]


def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return pd.read_csv(path)


def add_row(rows, category, item, status, details=""):
    rows.append(
        {
            "category": category,
            "item": item,
            "status": status,
            "details": details,
        }
    )


def check_file_exists(rows, category, path):
    p = Path(path)
    if p.exists():
        add_row(rows, category, path, "PASS", "exists")
    else:
        add_row(rows, category, path, "FAIL", "missing")


def check_dataset(rows, dataset):
    path = Path(dataset["path"])

    if not path.exists():
        add_row(rows, "dataset", dataset["name"], "FAIL", f"missing file: {path}")
        return

    try:
        df = read_csv_safe(path)
    except Exception as e:
        add_row(rows, "dataset", dataset["name"], "FAIL", f"cannot read CSV: {e}")
        return

    expected_rows = dataset["expected_rows"]

    if expected_rows is not None and len(df) != expected_rows:
        add_row(
            rows,
            "dataset",
            dataset["name"],
            "WARN",
            f"row count = {len(df)}, expected = {expected_rows}",
        )
    else:
        add_row(
            rows,
            "dataset",
            dataset["name"],
            "PASS",
            f"row count = {len(df)}",
        )

    missing_cols = [c for c in dataset["required_columns"] if c not in df.columns]

    if missing_cols:
        add_row(
            rows,
            "dataset_columns",
            dataset["name"],
            "FAIL",
            f"missing columns: {missing_cols}",
        )
    else:
        add_row(
            rows,
            "dataset_columns",
            dataset["name"],
            "PASS",
            "required columns present",
        )

    if "masculine_sentence" in df.columns and "feminine_sentence" in df.columns:
        empty_m = int(df["masculine_sentence"].isna().sum())
        empty_f = int(df["feminine_sentence"].isna().sum())

        if empty_m == 0 and empty_f == 0:
            add_row(rows, "dataset_sentences", dataset["name"], "PASS", "no empty sentence cells")
        else:
            add_row(
                rows,
                "dataset_sentences",
                dataset["name"],
                "FAIL",
                f"empty masculine={empty_m}, empty feminine={empty_f}",
            )

    for col in ["dialect", "template_id", "template_type", "semantic_frame", "field", "department"]:
        if col in df.columns:
            add_row(
                rows,
                "dataset_structure",
                f"{dataset['name']}::{col}",
                "PASS",
                f"unique values = {df[col].nunique(dropna=True)}",
            )


def check_score_difference_validation(rows):
    path = Path("results/final_package/score_difference_validation_report.csv")

    if not path.exists():
        add_row(rows, "validation", "score_difference_validation", "FAIL", "missing report")
        return

    df = read_csv_safe(path)

    if "status" not in df.columns:
        add_row(rows, "validation", "score_difference_validation", "FAIL", "missing status column")
        return

    failed = df[df["status"].astype(str).str.lower() != "pass"]

    formula_errors = 0
    pref_errors = 0

    for col in ["formula_error_rows", "formula_incorrect_rows"]:
        if col in df.columns:
            formula_errors += int(pd.to_numeric(df[col], errors="coerce").fillna(0).sum())

    for col in ["preference_label_error_rows", "preference_label_errors"]:
        if col in df.columns:
            pref_errors += int(pd.to_numeric(df[col], errors="coerce").fillna(0).sum())

    if failed.empty and formula_errors == 0 and pref_errors == 0:
        add_row(rows, "validation", "score_difference_validation", "PASS", "all checked files passed")
    else:
        add_row(
            rows,
            "validation",
            "score_difference_validation",
            "FAIL",
            f"failed files={len(failed)}, formula_errors={formula_errors}, preference_errors={pref_errors}",
        )


def check_formula_validation(rows):
    path = Path("results/q1_formula_validation/q1_formula_validation_report.csv")

    if not path.exists():
        add_row(rows, "validation", "q1_formula_validation", "FAIL", "missing report")
        return

    df = read_csv_safe(path)

    if "status" not in df.columns:
        add_row(rows, "validation", "q1_formula_validation", "FAIL", "missing status column")
        return

    failed = df[df["status"].astype(str).str.lower() == "fail"]

    if failed.empty:
        add_row(rows, "validation", "q1_formula_validation", "PASS", "no failed formula checks")
    else:
        add_row(rows, "validation", "q1_formula_validation", "FAIL", f"failed rows={len(failed)}")


def check_v6_quality(rows):
    path = Path("results/occupational_benchmark_v6_job_roles_quality/v6_quality_summary.csv")

    if not path.exists():
        add_row(rows, "quality", "v6_quality_summary", "FAIL", "missing")
        return

    text = path.read_text(encoding="utf-8-sig", errors="ignore").lower()

    if "no_issues_found" in text:
        add_row(rows, "quality", "v6_quality_summary", "PASS", "no_issues_found")
    else:
        add_row(rows, "quality", "v6_quality_summary", "WARN", "review quality summary")


def check_mitigation(rows):
    path = Path("results/q1_bias_mitigation/q1_bias_mitigation_effect_summary.csv")

    if not path.exists():
        add_row(rows, "mitigation", "q1_bias_mitigation_effect_summary", "FAIL", "missing")
        return

    df = read_csv_safe(path)

    if "status" not in df.columns:
        add_row(rows, "mitigation", "q1_bias_mitigation_effect_summary", "FAIL", "missing status column")
        return

    compared = int((df["status"].astype(str) == "compared").sum())
    missing = int((df["status"].astype(str) != "compared").sum())

    if compared > 0 and missing == 0:
        add_row(rows, "mitigation", "q1_bias_mitigation_effect_summary", "PASS", f"comparisons completed={compared}")
    elif compared > 0:
        add_row(rows, "mitigation", "q1_bias_mitigation_effect_summary", "WARN", f"completed={compared}, missing={missing}")
    else:
        add_row(rows, "mitigation", "q1_bias_mitigation_effect_summary", "FAIL", "no completed comparisons")


def check_human_validation(rows):
    sheet = Path("data/human_validation/q1_validation/q1_human_validation_annotation_sheet.csv")
    agreement = Path("results/human_validation/q1_validation/q1_human_validation_agreement_summary.csv")

    if not sheet.exists():
        add_row(rows, "human_validation", "annotation_sheet", "FAIL", "missing")
    else:
        df = read_csv_safe(sheet)
        if len(df) >= 500:
            add_row(rows, "human_validation", "annotation_sheet", "PASS", f"rows={len(df)}")
        else:
            add_row(rows, "human_validation", "annotation_sheet", "WARN", f"rows={len(df)}, target=500")

    if not agreement.exists():
        add_row(rows, "human_validation", "agreement_summary", "WARN", "missing until annotators finish")
    else:
        df = read_csv_safe(agreement)
        if "cohens_kappa" in df.columns:
            add_row(rows, "human_validation", "agreement_summary", "PASS", "Cohen's Kappa report exists")
        else:
            add_row(rows, "human_validation", "agreement_summary", "WARN", "agreement file exists but no cohens_kappa column")


def check_python_compile(rows, path):
    p = Path(path)

    if not p.exists():
        add_row(rows, "python_compile", path, "FAIL", "missing")
        return

    try:
        py_compile.compile(str(p), doraise=True)
        add_row(rows, "python_compile", path, "PASS", "syntax ok")
    except Exception as e:
        add_row(rows, "python_compile", path, "FAIL", str(e))


def run_git_command(args):
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            shell=False,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def check_git(rows):
    code, stdout, stderr = run_git_command(["git", "status", "--short"])

    if code != 0:
        add_row(rows, "git", "git_status", "FAIL", stderr)
        return

    if stdout.strip() == "":
        add_row(rows, "git", "git_status", "PASS", "working tree clean")
    else:
        add_row(rows, "git", "git_status", "WARN", stdout.replace("\n", " | "))

    code, stdout, stderr = run_git_command(["git", "ls-files", "data/external_datasets/arabjobs/ArabJobs.csv"])

    if code == 0 and stdout.strip() == "":
        add_row(rows, "git", "raw_arabjobs_not_tracked", "PASS", "ArabJobs.csv is not tracked")
    elif code == 0:
        add_row(rows, "git", "raw_arabjobs_not_tracked", "WARN", "ArabJobs.csv is tracked")
    else:
        add_row(rows, "git", "raw_arabjobs_not_tracked", "WARN", stderr)


def check_gitignore(rows):
    path = Path(".gitignore")

    if not path.exists():
        add_row(rows, "gitignore", ".gitignore", "WARN", "missing")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")

    checks = {
        "ArabJobs.csv ignored": "data/external_datasets/arabjobs/ArabJobs.csv",
        "models ignored": "models/",
        "python cache ignored": "__pycache__/",
    }

    for label, pattern in checks.items():
        if pattern in text:
            add_row(rows, "gitignore", label, "PASS", pattern)
        else:
            add_row(rows, "gitignore", label, "WARN", f"missing pattern: {pattern}")


def write_markdown(report_df):
    total = len(report_df)
    passed = int((report_df["status"] == "PASS").sum())
    warned = int((report_df["status"] == "WARN").sum())
    failed = int((report_df["status"] == "FAIL").sum())

    lines = []
    lines.append("# Full Q1 Project Audit Summary")
    lines.append("")
    lines.append("## Overall Status")
    lines.append("")
    lines.append(f"- Total checks: {total}")
    lines.append(f"- Passed: {passed}")
    lines.append(f"- Warnings: {warned}")
    lines.append(f"- Failed: {failed}")
    lines.append("")

    if failed == 0:
        lines.append("## Conclusion")
        lines.append("")
        lines.append("The project passed the full audit with no failed checks.")
        lines.append("")
    else:
        lines.append("## Conclusion")
        lines.append("")
        lines.append("The project has failed checks that must be reviewed before final submission.")
        lines.append("")

    for status in ["FAIL", "WARN"]:
        subset = report_df[report_df["status"] == status]
        if subset.empty:
            continue

        lines.append(f"## {status} Items")
        lines.append("")

        for _, row in subset.iterrows():
            lines.append(f"- **{row['category']}** | `{row['item']}` | {row['details']}")
        lines.append("")

    lines.append("## Passed Categories")
    lines.append("")

    passed_summary = (
        report_df[report_df["status"] == "PASS"]
        .groupby("category")
        .size()
        .reset_index(name="passed_checks")
    )

    for _, row in passed_summary.iterrows():
        lines.append(f"- {row['category']}: {row['passed_checks']}")

    lines.append("")
    lines.append("## Audit Report File")
    lines.append("")
    lines.append(f"- `{AUDIT_CSV}`")
    lines.append("")

    AUDIT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    for dataset in EXPECTED_DATASETS:
        check_dataset(rows, dataset)

    for path in EXPECTED_RESULT_FILES:
        check_file_exists(rows, "result_file", path)

    for path in EXPECTED_DOCS:
        check_file_exists(rows, "doc_file", path)

    for path in EXPECTED_SOFTWARE_FILES:
        check_file_exists(rows, "software_file", path)

    for path in EXPECTED_SCRIPTS:
        check_file_exists(rows, "script_file", path)
        check_python_compile(rows, path)

    check_python_compile(rows, "software_bias_measurement/app.py")
    check_python_compile(rows, "software_dashboard/app.py")

    check_score_difference_validation(rows)
    check_formula_validation(rows)
    check_v6_quality(rows)
    check_mitigation(rows)
    check_human_validation(rows)
    check_gitignore(rows)
    check_git(rows)

    report_df = pd.DataFrame(rows)
    report_df.to_csv(AUDIT_CSV, index=False, encoding="utf-8-sig")

    write_markdown(report_df)

    print("Full Q1 project audit completed.")
    print("CSV:", AUDIT_CSV)
    print("Markdown:", AUDIT_MD)
    print("")
    print(report_df["status"].value_counts().to_string())
    print("")
    print("Failed/Warn items:")
    failed_warn = report_df[report_df["status"].isin(["FAIL", "WARN"])]
    if failed_warn.empty:
        print("None")
    else:
        print(failed_warn.to_string(index=False))


if __name__ == "__main__":
    main()