from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/q1_bias_mitigation")
OUTPUT_CSV = OUTPUT_DIR / "q1_bias_mitigation_effect_summary.csv"
DOC_PATH = Path("docs/occupational_scope/q1_bias_mitigation_effect_summary.md")


BASE_MODEL = "aubmindlab/aragpt2-base"

COMPARISONS = [
    {
        "benchmark": "v2_main",
        "before_keywords": ["v2"],
        "after_analysis": Path("results/q1_bias_mitigation/analysis_mitigated_aragpt2_base_v2/summary_overall.csv"),
        "after_scoring_dir": Path("results/q1_bias_mitigation/scoring_mitigated_aragpt2_base_v2"),
    },
    {
        "benchmark": "v5_job_titles",
        "before_keywords": ["v5"],
        "after_analysis": Path("results/q1_bias_mitigation/analysis_mitigated_aragpt2_base_v5/summary_overall.csv"),
        "after_scoring_dir": Path("results/q1_bias_mitigation/scoring_mitigated_aragpt2_base_v5"),
    },
    {
        "benchmark": "v6_job_roles_departments",
        "before_keywords": ["v6"],
        "after_analysis": Path("results/q1_bias_mitigation/analysis_mitigated_aragpt2_base_v6/summary_overall.csv"),
        "after_scoring_dir": Path("results/q1_bias_mitigation/scoring_mitigated_aragpt2_base_v6"),
    },
    {
        "benchmark": "arabjobs_v7_external",
        "before_keywords": ["arabjobs"],
        "after_analysis": Path("results/q1_bias_mitigation/analysis_mitigated_aragpt2_base_arabjobs_v7/summary_overall.csv"),
        "after_scoring_dir": Path("results/q1_bias_mitigation/scoring_mitigated_aragpt2_base_arabjobs_v7"),
    },
]


def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return pd.read_csv(path)


def pct(value, total):
    if total == 0:
        return 0.0
    return float((value / total) * 100)


def classify(avg):
    try:
        avg = float(avg)
    except Exception:
        return "unknown"

    if avg > 0.05:
        return "masculine"
    if avg < -0.05:
        return "feminine"
    return "near-neutral_or_mixed"


def clean_percent(value):
    if pd.isna(value):
        return 0.0

    text = str(value).replace("%", "").strip()

    try:
        return float(text)
    except Exception:
        return 0.0


def get_numeric(row, col, default=0.0):
    if col not in row.index:
        return default

    value = row[col]

    if isinstance(value, str) and "%" in value:
        return clean_percent(value)

    try:
        return float(value)
    except Exception:
        return default


def summarize_scoring_file(path):
    df = read_csv_safe(path)

    required = ["score_difference", "preferred_gender"]
    if not all(col in df.columns for col in required):
        return None

    temp = df.copy()
    temp["score_difference"] = pd.to_numeric(temp["score_difference"], errors="coerce")
    temp = temp.dropna(subset=["score_difference"])

    if temp.empty:
        return None

    total = len(temp)
    masculine = int((temp["preferred_gender"].astype(str).str.lower() == "masculine").sum())
    feminine = int((temp["preferred_gender"].astype(str).str.lower() == "feminine").sum())
    equal = int((temp["preferred_gender"].astype(str).str.lower() == "equal").sum())

    return {
        "model_name": str(temp["model_name"].iloc[0]) if "model_name" in temp.columns else "unknown",
        "total_items": total,
        "masculine_preferred_count": masculine,
        "feminine_preferred_count": feminine,
        "equal_count": equal,
        "masculine_preferred_percent": pct(masculine, total),
        "feminine_preferred_percent": pct(feminine, total),
        "equal_percent": pct(equal, total),
        "average_score_difference": float(temp["score_difference"].mean()),
        "median_score_difference": float(temp["score_difference"].median()),
        "min_score_difference": float(temp["score_difference"].min()),
        "max_score_difference": float(temp["score_difference"].max()),
    }


def get_summary_row_from_file(path, preferred_model=None):
    if not path.exists():
        return None

    df = read_csv_safe(path)

    if "average_score_difference" not in df.columns:
        return None

    if preferred_model and "model_name" in df.columns:
        selected = df[df["model_name"].astype(str).str.strip() == preferred_model]
        if not selected.empty:
            return selected.iloc[0].to_dict()

    return df.iloc[0].to_dict()


def get_after_summary(comp):
    row = get_summary_row_from_file(comp["after_analysis"])

    if row is not None:
        return row, str(comp["after_analysis"])

    scoring_dir = comp["after_scoring_dir"]

    if scoring_dir.exists():
        scoring_files = list(scoring_dir.glob("scoring_results_occupational_v1_*.csv"))
        if scoring_files:
            row = summarize_scoring_file(scoring_files[0])
            if row is not None:
                return row, str(scoring_files[0])

    return None, ""


def find_before_summary(comp):
    keywords = [k.lower() for k in comp["before_keywords"]]
    candidates = []

    for path in Path("results").rglob("*.csv"):
        path_text = str(path).lower()

        if not all(k in path_text for k in keywords):
            continue

        if "q1_bias_mitigation" in path_text:
            continue

        try:
            df = read_csv_safe(path)
        except Exception:
            continue

        if "average_score_difference" not in df.columns:
            continue

        if "model_name" in df.columns:
            selected = df[df["model_name"].astype(str).str.strip() == BASE_MODEL]
            if selected.empty:
                continue

            score = 0
            if "combined_analysis" in path_text:
                score += 5
            if "overall" in path.name.lower():
                score += 5
            if "summary_overall" in path.name.lower():
                score += 4
            if "by_model" in path.name.lower():
                score += 4

            candidates.append((score, path, selected.iloc[0].to_dict()))

    if not candidates:
        return None, ""

    candidates = sorted(candidates, key=lambda x: x[0], reverse=True)
    return candidates[0][2], str(candidates[0][1])


def compare_rows(benchmark, before_row, after_row, before_file, after_file):
    before_avg = get_numeric(pd.Series(before_row), "average_score_difference")
    after_avg = get_numeric(pd.Series(after_row), "average_score_difference")

    before_abs = abs(before_avg)
    after_abs = abs(after_avg)

    mitigation_gain = before_abs - after_abs

    before_m = clean_percent(before_row.get("masculine_preferred_percent", 0))
    after_m = clean_percent(after_row.get("masculine_preferred_percent", 0))

    before_f = clean_percent(before_row.get("feminine_preferred_percent", 0))
    after_f = clean_percent(after_row.get("feminine_preferred_percent", 0))

    return {
        "benchmark": benchmark,
        "status": "compared",
        "before_file": before_file,
        "after_file": after_file,
        "before_model": BASE_MODEL,
        "after_model": after_row.get("model_name", "models/q1_mitigation/aragpt2_base_counterfactual_cda"),
        "before_total_items": get_numeric(pd.Series(before_row), "total_items"),
        "after_total_items": get_numeric(pd.Series(after_row), "total_items"),
        "before_average_score_difference": before_avg,
        "after_average_score_difference": after_avg,
        "before_direction": classify(before_avg),
        "after_direction": classify(after_avg),
        "before_absolute_bias": before_abs,
        "after_absolute_bias": after_abs,
        "mitigation_gain_abs_bias": mitigation_gain,
        "bias_reduced": mitigation_gain > 0,
        "before_masculine_preferred_percent": before_m,
        "after_masculine_preferred_percent": after_m,
        "before_feminine_preferred_percent": before_f,
        "after_feminine_preferred_percent": after_f,
        "masculine_percent_change": after_m - before_m,
        "feminine_percent_change": after_f - before_f,
    }


def write_doc(result_df):
    doc = []

    doc.append("# Q1 Bias Mitigation Effect Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This analysis compares AraGPT2-base before and after counterfactual data augmentation fine-tuning."
    )
    doc.append("")
    doc.append("## Mitigation Formula")
    doc.append("")
    doc.append("Mitigation_Gain = |Bias_before| - |Bias_after|")
    doc.append("")
    doc.append("A positive mitigation gain means the absolute directional bias decreased after fine-tuning.")
    doc.append("")
    doc.append("## Output")
    doc.append("")
    doc.append(f"- CSV: `{OUTPUT_CSV}`")
    doc.append("")
    doc.append("## Results")
    doc.append("")

    for _, row in result_df.iterrows():
        doc.append(f"### {row['benchmark']}")
        doc.append("")
        doc.append(f"- Status: {row['status']}")

        if row["status"] == "compared":
            doc.append(f"- Before average score_difference: {row['before_average_score_difference']}")
            doc.append(f"- After average score_difference: {row['after_average_score_difference']}")
            doc.append(f"- Before direction: {row['before_direction']}")
            doc.append(f"- After direction: {row['after_direction']}")
            doc.append(f"- Mitigation gain: {row['mitigation_gain_abs_bias']}")
            doc.append(f"- Bias reduced: {row['bias_reduced']}")
            doc.append(f"- Before file: `{row['before_file']}`")
            doc.append(f"- After file: `{row['after_file']}`")
        else:
            doc.append(f"- Missing reason: {row.get('missing_reason', '')}")

        doc.append("")

    doc.append("## Publication Claim")
    doc.append("")
    doc.append(
        "This experiment extends the framework from bias measurement to bias mitigation by testing whether balanced "
        "Arabic masculine-feminine counterfactual fine-tuning reduces measured occupational gender preference."
    )
    doc.append("")
    doc.append("## Limitation")
    doc.append("")
    doc.append(
        "This experiment does not claim to remove gender bias completely. It evaluates whether one controlled "
        "counterfactual fine-tuning intervention reduces measured bias under the proposed paired-likelihood metric."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for comp in COMPARISONS:
        benchmark = comp["benchmark"]

        before_row, before_file = find_before_summary(comp)
        after_row, after_file = get_after_summary(comp)

        if before_row is None or after_row is None:
            rows.append({
                "benchmark": benchmark,
                "status": "missing_input",
                "before_found": before_row is not None,
                "after_found": after_row is not None,
                "before_file": before_file,
                "after_file": after_file,
                "missing_reason": "before_summary_missing_or_after_summary_missing",
            })
            continue

        rows.append(
            compare_rows(
                benchmark=benchmark,
                before_row=before_row,
                after_row=after_row,
                before_file=before_file,
                after_file=after_file,
            )
        )

    result_df = pd.DataFrame(rows)
    result_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    write_doc(result_df)

    print("Q1 bias mitigation effect analysis completed.")
    print("CSV:", OUTPUT_CSV)
    print("DOC:", DOC_PATH)
    print("")
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    main()