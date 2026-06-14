from pathlib import Path
import argparse
import pandas as pd


def normalize_yes_no(value):
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    if value in ["yes", "y", "true", "1", "نعم", "اه", "أه"]:
        return "yes"

    if value in ["no", "n", "false", "0", "لا"]:
        return "no"

    return value


def normalize_decision(value):
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    if value in ["keep", "k", "احتفظ", "تمام"]:
        return "keep"

    if value in ["revise", "r", "edit", "تعديل"]:
        return "revise"

    if value in ["remove", "delete", "حذف"]:
        return "remove"

    return value


def to_numeric_score(series):
    return pd.to_numeric(series, errors="coerce")


def summarize_group(df, group_cols):
    rows = []

    for group_values, group_df in df.groupby(group_cols):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        row = {}

        for col, value in zip(group_cols, group_values):
            row[col] = value

        total = len(group_df)

        keep_count = int((group_df["final_decision_keep_revise_remove_norm"] == "keep").sum())
        revise_count = int((group_df["final_decision_keep_revise_remove_norm"] == "revise").sum())
        remove_count = int((group_df["final_decision_keep_revise_remove_norm"] == "remove").sum())

        dialect_yes = int((group_df["dialect_correct_yes_no_norm"] == "yes").sum())
        gender_yes = int((group_df["gender_pair_correct_yes_no_norm"] == "yes").sum())
        field_yes = int((group_df["occupation_field_correct_yes_no_norm"] == "yes").sum())

        row.update({
            "total_rows": total,
            "avg_naturalness_masculine": group_df["naturalness_masculine_1_to_5_num"].mean(),
            "avg_naturalness_feminine": group_df["naturalness_feminine_1_to_5_num"].mean(),
            "avg_meaning_equivalence": group_df["meaning_equivalence_1_to_5_num"].mean(),
            "dialect_correct_percent": dialect_yes / total * 100 if total else 0,
            "gender_pair_correct_percent": gender_yes / total * 100 if total else 0,
            "occupation_field_correct_percent": field_yes / total * 100 if total else 0,
            "keep_count": keep_count,
            "revise_count": revise_count,
            "remove_count": remove_count,
            "keep_percent": keep_count / total * 100 if total else 0,
            "revise_percent": revise_count / total * 100 if total else 0,
            "remove_percent": remove_count / total * 100 if total else 0,
        })

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Filled human validation CSV file.",
    )

    parser.add_argument(
        "--output_dir",
        default="results/occupational_benchmark_v1/human_validation_analysis",
        help="Output directory.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "id",
        "field",
        "dialect",
        "template_id",
        "occupation_id",
        "occupation_m",
        "occupation_f",
        "naturalness_masculine_1_to_5",
        "naturalness_feminine_1_to_5",
        "meaning_equivalence_1_to_5",
        "dialect_correct_yes_no",
        "gender_pair_correct_yes_no",
        "occupation_field_correct_yes_no",
        "final_decision_keep_revise_remove",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["naturalness_masculine_1_to_5_num"] = to_numeric_score(df["naturalness_masculine_1_to_5"])
    df["naturalness_feminine_1_to_5_num"] = to_numeric_score(df["naturalness_feminine_1_to_5"])
    df["meaning_equivalence_1_to_5_num"] = to_numeric_score(df["meaning_equivalence_1_to_5"])

    df["dialect_correct_yes_no_norm"] = df["dialect_correct_yes_no"].apply(normalize_yes_no)
    df["gender_pair_correct_yes_no_norm"] = df["gender_pair_correct_yes_no"].apply(normalize_yes_no)
    df["occupation_field_correct_yes_no_norm"] = df["occupation_field_correct_yes_no"].apply(normalize_yes_no)
    df["final_decision_keep_revise_remove_norm"] = df["final_decision_keep_revise_remove"].apply(normalize_decision)

    df["auto_quality_pass"] = (
        (df["naturalness_masculine_1_to_5_num"] >= 4)
        & (df["naturalness_feminine_1_to_5_num"] >= 4)
        & (df["meaning_equivalence_1_to_5_num"] >= 4)
        & (df["dialect_correct_yes_no_norm"] == "yes")
        & (df["gender_pair_correct_yes_no_norm"] == "yes")
    )

    df.to_csv(
        output_dir / "human_validation_normalized.csv",
        index=False,
        encoding="utf-8-sig",
    )

    overall_summary = pd.DataFrame([{
        "total_rows": len(df),
        "avg_naturalness_masculine": df["naturalness_masculine_1_to_5_num"].mean(),
        "avg_naturalness_feminine": df["naturalness_feminine_1_to_5_num"].mean(),
        "avg_meaning_equivalence": df["meaning_equivalence_1_to_5_num"].mean(),
        "auto_quality_pass_count": int(df["auto_quality_pass"].sum()),
        "auto_quality_pass_percent": df["auto_quality_pass"].mean() * 100,
        "keep_count": int((df["final_decision_keep_revise_remove_norm"] == "keep").sum()),
        "revise_count": int((df["final_decision_keep_revise_remove_norm"] == "revise").sum()),
        "remove_count": int((df["final_decision_keep_revise_remove_norm"] == "remove").sum()),
    }])

    overall_summary.to_csv(
        output_dir / "human_validation_overall_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summarize_group(df, ["field"]).to_csv(
        output_dir / "human_validation_by_field.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summarize_group(df, ["dialect"]).to_csv(
        output_dir / "human_validation_by_dialect.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summarize_group(df, ["template_id"]).to_csv(
        output_dir / "human_validation_by_template.csv",
        index=False,
        encoding="utf-8-sig",
    )

    needs_review = df[
        (df["auto_quality_pass"] == False)
        | (df["final_decision_keep_revise_remove_norm"].isin(["revise", "remove"]))
    ]

    needs_review.to_csv(
        output_dir / "human_validation_rows_needing_review.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Human validation analysis completed.")
    print("Outputs saved to:")
    print(output_dir)
    print("\nOverall summary:")
    print(overall_summary)


if __name__ == "__main__":
    main()