from pathlib import Path
import pandas as pd


SEARCH_ROOT = Path("results")
OUTPUT_PATH = Path("results/final_package/score_difference_validation_report.csv")
DOC_PATH = Path("docs/occupational_scope/score_difference_validation_summary.md")

TOLERANCE = 1e-6


def expected_preference(diff):
    if diff > TOLERANCE:
        return "masculine"
    if diff < -TOLERANCE:
        return "feminine"
    return "equal"


def normalize_pref(value):
    value = str(value).strip().lower()
    if value in ["masculine", "male", "m"]:
        return "masculine"
    if value in ["feminine", "female", "f"]:
        return "feminine"
    if value in ["equal", "tie", "neutral", "same"]:
        return "equal"
    return value


def validate_file(path):
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return None

    required = ["masculine_score", "feminine_score", "score_difference"]
    if not all(col in df.columns for col in required):
        return None

    temp = df.copy()
    for col in required:
        temp[col] = pd.to_numeric(temp[col], errors="coerce")

    temp = temp.dropna(subset=required)

    if temp.empty:
        return None

    recomputed = temp["masculine_score"] - temp["feminine_score"]
    error = (recomputed - temp["score_difference"]).abs()

    formula_incorrect = int((error > TOLERANCE).sum())

    preference_errors = ""

    if "preferred_gender" in temp.columns:
        expected = recomputed.apply(expected_preference)
        actual = temp["preferred_gender"].apply(normalize_pref)
        preference_errors = int((expected != actual).sum())

    return {
        "file_path": str(path),
        "rows_checked": len(temp),
        "formula_correct_rows": int((error <= TOLERANCE).sum()),
        "formula_incorrect_rows": formula_incorrect,
        "max_absolute_formula_error": float(error.max()),
        "preference_label_errors": preference_errors,
        "status": "pass" if formula_incorrect == 0 and preference_errors in [0, ""] else "needs_review",
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for path in SEARCH_ROOT.glob("**/*.csv"):
        result = validate_file(path)
        if result:
            rows.append(result)

    if not rows:
        raise RuntimeError("No scoring CSV files found with masculine_score, feminine_score, and score_difference columns.")

    report = pd.DataFrame(rows)
    report.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    total_files = len(report)
    passed_files = int((report["status"] == "pass").sum())
    review_files = total_files - passed_files

    doc = []
    doc.append("# Score Difference Validation Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append("This validation verifies that score_difference is implemented consistently as masculine_score minus feminine_score.")
    doc.append("")
    doc.append("## Validation Rule")
    doc.append("")
    doc.append("score_difference = masculine_score - feminine_score")
    doc.append("")
    doc.append("## Preference Rule")
    doc.append("")
    doc.append("- positive score_difference = masculine preference")
    doc.append("- negative score_difference = feminine preference")
    doc.append("- zero score_difference = equal preference")
    doc.append("")
    doc.append("## Summary")
    doc.append("")
    doc.append(f"- Files checked: {total_files}")
    doc.append(f"- Files passed: {passed_files}")
    doc.append(f"- Files needing review: {review_files}")
    doc.append("")
    doc.append("## Output")
    doc.append("")
    doc.append(f"- Detailed validation report: `{OUTPUT_PATH}`")
    doc.append("")
    doc.append("## Thesis Use")
    doc.append("")
    doc.append("This validation provides implementation-level evidence that the score_difference equation was applied correctly across model scoring outputs.")

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("Score difference validation completed.")
    print("Report:", OUTPUT_PATH)
    print("Summary:", DOC_PATH)
    print(report[["file_path", "rows_checked", "formula_incorrect_rows", "preference_label_errors", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()