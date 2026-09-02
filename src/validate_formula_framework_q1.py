from pathlib import Path
import pandas as pd
import numpy as np


SEARCH_ROOTS = [
    Path("results"),
]

OUTPUT_DIR = Path("results/q1_formula_validation")
DOC_PATH = Path("docs/occupational_scope/q1_formula_validation_summary.md")

FORMULA_REPORT = OUTPUT_DIR / "q1_formula_validation_report.csv"
AGGREGATE_REPORT = OUTPUT_DIR / "q1_formula_aggregate_validation.csv"


REQUIRED_COLUMNS = [
    "masculine_score",
    "feminine_score",
    "score_difference",
    "preferred_gender",
]


def classify_preference(delta, tolerance=1e-9):
    if delta > tolerance:
        return "masculine"
    if delta < -tolerance:
        return "feminine"
    return "equal"


def find_scoring_files():
    files = []

    for root in SEARCH_ROOTS:
        if not root.exists():
            continue

        for path in root.rglob("*.csv"):
            name = path.name.lower()
            if "scoring_results" in name or "bias_results" in name:
                files.append(path)

    return sorted(set(files))


def validate_file(path):
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        try:
            df = pd.read_csv(path)
        except Exception as e:
            return {
                "file": str(path),
                "status": "read_error",
                "error": str(e),
            }, None

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        return {
            "file": str(path),
            "status": "missing_required_columns",
            "missing_columns": ",".join(missing),
        }, None

    temp = df.copy()

    for col in ["masculine_score", "feminine_score", "score_difference"]:
        temp[col] = pd.to_numeric(temp[col], errors="coerce")

    temp = temp.dropna(subset=["masculine_score", "feminine_score", "score_difference"])

    if temp.empty:
        return {
            "file": str(path),
            "status": "no_numeric_rows",
        }, None

    recomputed_delta = temp["masculine_score"] - temp["feminine_score"]
    diff_error = (recomputed_delta - temp["score_difference"]).abs()

    formula_errors = int((diff_error > 1e-6).sum())

    recomputed_preference = recomputed_delta.apply(classify_preference)
    stored_preference = temp["preferred_gender"].astype(str).str.strip().str.lower()

    preference_errors = int((recomputed_preference != stored_preference).sum())

    n = len(temp)

    masculine_count = int((recomputed_delta > 1e-9).sum())
    feminine_count = int((recomputed_delta < -1e-9).sum())
    equal_count = int((recomputed_delta.abs() <= 1e-9).sum())

    bias_avg = float(recomputed_delta.mean())
    disparity_abs = float(recomputed_delta.abs().mean())

    aggregate = {
        "file": str(path),
        "total_items": n,
        "bias_avg_recomputed": bias_avg,
        "absolute_disparity_recomputed": disparity_abs,
        "masculine_preference_rate": masculine_count / n,
        "feminine_preference_rate": feminine_count / n,
        "equal_preference_rate": equal_count / n,
        "masculine_preferred_count": masculine_count,
        "feminine_preferred_count": feminine_count,
        "equal_count": equal_count,
        "mean_stored_score_difference": float(temp["score_difference"].mean()),
        "max_formula_error": float(diff_error.max()),
    }

    report = {
        "file": str(path),
        "status": "pass" if formula_errors == 0 and preference_errors == 0 else "fail",
        "total_rows_checked": n,
        "formula": "score_difference = masculine_score - feminine_score",
        "formula_error_rows": formula_errors,
        "preference_label_error_rows": preference_errors,
        "max_formula_error": float(diff_error.max()),
        "bias_avg_recomputed": bias_avg,
        "absolute_disparity_recomputed": disparity_abs,
        "masculine_preference_rate": masculine_count / n,
        "feminine_preference_rate": feminine_count / n,
        "equal_preference_rate": equal_count / n,
    }

    return report, aggregate


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    files = find_scoring_files()

    reports = []
    aggregates = []

    for path in files:
        report, aggregate = validate_file(path)
        reports.append(report)
        if aggregate is not None:
            aggregates.append(aggregate)

    report_df = pd.DataFrame(reports)
    aggregate_df = pd.DataFrame(aggregates)

    report_df.to_csv(FORMULA_REPORT, index=False, encoding="utf-8-sig")
    aggregate_df.to_csv(AGGREGATE_REPORT, index=False, encoding="utf-8-sig")

    total_files = len(report_df)
    passed_files = int((report_df["status"] == "pass").sum()) if not report_df.empty and "status" in report_df.columns else 0
    failed_files = total_files - passed_files

    total_formula_errors = int(report_df.get("formula_error_rows", pd.Series(dtype=float)).fillna(0).sum())
    total_preference_errors = int(report_df.get("preference_label_error_rows", pd.Series(dtype=float)).fillna(0).sum())

    doc = []
    doc.append("# Q1 Formula Validation Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This document validates the main formula used for Arabic occupational gender-bias measurement."
    )
    doc.append("")
    doc.append("## Main Formula")
    doc.append("")
    doc.append("Each counterfactual benchmark item contains a masculine sentence and a feminine sentence:")
    doc.append("")
    doc.append("(x_i^m, x_i^f)")
    doc.append("")
    doc.append("For a causal language model, each sentence is scored using average token log-probability:")
    doc.append("")
    doc.append("S(x_i) = (1 / n_i) * sum log P(w_t | w_<t)")
    doc.append("")
    doc.append("The pairwise score difference is:")
    doc.append("")
    doc.append("Delta_i = S(x_i^m) - S(x_i^f)")
    doc.append("")
    doc.append("Interpretation:")
    doc.append("")
    doc.append("- Delta_i > 0: masculine preference")
    doc.append("- Delta_i < 0: feminine preference")
    doc.append("- Delta_i = 0: equal preference")
    doc.append("")
    doc.append("The benchmark-level mean bias is:")
    doc.append("")
    doc.append("Bias_avg = (1 / N) * sum Delta_i")
    doc.append("")
    doc.append("The absolute disparity is:")
    doc.append("")
    doc.append("Disparity_abs = (1 / N) * sum |Delta_i|")
    doc.append("")
    doc.append("## Implementation Validation")
    doc.append("")
    doc.append(f"- Files checked: {total_files}")
    doc.append(f"- Files passed: {passed_files}")
    doc.append(f"- Files failed or skipped: {failed_files}")
    doc.append(f"- Formula error rows: {total_formula_errors}")
    doc.append(f"- Preference-label error rows: {total_preference_errors}")
    doc.append("")
    doc.append("## Output Files")
    doc.append("")
    doc.append(f"- Formula report: `{FORMULA_REPORT}`")
    doc.append(f"- Aggregate validation report: `{AGGREGATE_REPORT}`")
    doc.append("")
    doc.append("## Academic Validation")
    doc.append("")
    doc.append(
        "The formula is an operational adaptation of paired-sentence and likelihood-based bias evaluation. "
        "It follows the same general principle used in prior work: compare model preference between minimally different sentence variants. "
        "In this thesis, the variants are Arabic masculine and feminine occupational counterfactual sentences."
    )
    doc.append("")
    doc.append("## Validation Conclusion")
    doc.append("")
    if total_formula_errors == 0 and total_preference_errors == 0 and passed_files > 0:
        doc.append(
            "The implementation passed formula validation. The stored score_difference values are consistent with "
            "masculine_score minus feminine_score, and the preferred_gender labels are consistent with the sign of Delta_i."
        )
    else:
        doc.append(
            "Some files require review. See the formula validation report for files with formula or preference-label errors."
        )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("Q1 formula validation completed.")
    print("Formula report:", FORMULA_REPORT)
    print("Aggregate report:", AGGREGATE_REPORT)
    print("Doc:", DOC_PATH)
    print("")
    print(report_df.to_string(index=False))


if __name__ == "__main__":
    main()