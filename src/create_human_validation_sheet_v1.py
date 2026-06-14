from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v1.csv")
OUTPUT_DIR = Path("data/occupational_benchmark/human_validation")
OUTPUT_PATH = OUTPUT_DIR / "human_validation_sheet_v1.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    validation_df = df[
        [
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
        ]
    ].copy()

    validation_df["naturalness_masculine_1_to_5"] = ""
    validation_df["naturalness_feminine_1_to_5"] = ""
    validation_df["meaning_equivalence_1_to_5"] = ""
    validation_df["dialect_correct_yes_no"] = ""
    validation_df["gender_pair_correct_yes_no"] = ""
    validation_df["occupation_field_correct_yes_no"] = ""
    validation_df["suggested_fix_masculine"] = ""
    validation_df["suggested_fix_feminine"] = ""
    validation_df["annotator_comments"] = ""
    validation_df["final_decision_keep_revise_remove"] = ""

    validation_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Human validation sheet created:")
    print(OUTPUT_PATH)
    print("Rows:", len(validation_df))
    print("Columns:", len(validation_df.columns))


if __name__ == "__main__":
    main()