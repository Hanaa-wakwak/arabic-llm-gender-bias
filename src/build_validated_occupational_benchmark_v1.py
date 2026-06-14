from pathlib import Path
import argparse
import pandas as pd


ORIGINAL_BENCHMARK_PATH = Path("data/occupational_benchmark/occupational_bias_v1.csv")


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


def add_missing_original_columns(validation_df):
    """
    Human validation sheets may not include workplace or notes.
    This function restores them from the original benchmark using id.
    """
    if not ORIGINAL_BENCHMARK_PATH.exists():
        return validation_df

    original_df = pd.read_csv(ORIGINAL_BENCHMARK_PATH, encoding="utf-8-sig")

    columns_to_restore = ["id"]

    for col in ["workplace", "notes"]:
        if col in original_df.columns and col not in validation_df.columns:
            columns_to_restore.append(col)

    if len(columns_to_restore) > 1:
        validation_df = validation_df.merge(
            original_df[columns_to_restore],
            on="id",
            how="left",
        )

    if "notes" not in validation_df.columns:
        validation_df["notes"] = "occupational_bias_v1_validated"

    return validation_df


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Filled human validation CSV file.",
    )

    parser.add_argument(
        "--output",
        default="data/occupational_benchmark/occupational_bias_v1_validated.csv",
        help="Output validated benchmark CSV.",
    )

    parser.add_argument(
        "--review_output",
        default="data/occupational_benchmark/human_validation/validated_rows_needing_manual_review.csv",
        help="Rows that still need manual review.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    review_output_path = Path(args.review_output)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    review_output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")
    df = add_missing_original_columns(df)

    required_columns = [
        "id",
        "field",
        "occupation_id",
        "occupation_m",
        "occupation_f",
        "dialect",
        "template_id",
        "masculine_sentence",
        "feminine_sentence",
        "stereotype_direction",
        "suggested_fix_masculine",
        "suggested_fix_feminine",
        "final_decision_keep_revise_remove",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["decision_norm"] = df["final_decision_keep_revise_remove"].apply(normalize_decision)

    validated_rows = []
    review_rows = []

    for _, row in df.iterrows():
        decision = row["decision_norm"]

        if decision == "remove":
            continue

        new_row = row.copy()

        if decision == "revise":
            suggested_m = (
                str(row["suggested_fix_masculine"]).strip()
                if not pd.isna(row["suggested_fix_masculine"])
                else ""
            )

            suggested_f = (
                str(row["suggested_fix_feminine"]).strip()
                if not pd.isna(row["suggested_fix_feminine"])
                else ""
            )

            if suggested_m:
                new_row["masculine_sentence"] = suggested_m

            if suggested_f:
                new_row["feminine_sentence"] = suggested_f

            if not suggested_m or not suggested_f:
                review_rows.append(row)

        elif decision == "keep":
            pass

        else:
            review_rows.append(row)

        validated_rows.append(new_row)

    validated_df = pd.DataFrame(validated_rows)

    output_columns = [
        "id",
        "field",
        "occupation_id",
        "occupation_m",
        "occupation_f",
        "workplace",
        "dialect",
        "template_id",
        "masculine_sentence",
        "feminine_sentence",
        "stereotype_direction",
        "notes",
    ]

    existing_output_columns = [col for col in output_columns if col in validated_df.columns]
    validated_df = validated_df[existing_output_columns]

    validated_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    review_df = pd.DataFrame(review_rows)
    review_df.to_csv(review_output_path, index=False, encoding="utf-8-sig")

    print("Validated benchmark created:")
    print(output_path)
    print("Validated rows:", len(validated_df))

    print("\nRows needing manual review:")
    print(review_output_path)
    print("Review rows:", len(review_df))

    print("\nDecision counts:")
    print(df["decision_norm"].value_counts(dropna=False))


if __name__ == "__main__":
    main()