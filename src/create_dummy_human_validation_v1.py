from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/human_validation/human_validation_sheet_v1.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/human_validation/human_validation_sheet_v1_dummy_filled.csv")


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    df["naturalness_masculine_1_to_5"] = 5
    df["naturalness_feminine_1_to_5"] = 5
    df["meaning_equivalence_1_to_5"] = 5
    df["dialect_correct_yes_no"] = "yes"
    df["gender_pair_correct_yes_no"] = "yes"
    df["occupation_field_correct_yes_no"] = "yes"
    df["suggested_fix_masculine"] = ""
    df["suggested_fix_feminine"] = ""
    df["annotator_comments"] = ""
    df["final_decision_keep_revise_remove"] = "keep"

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Dummy filled validation sheet created:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()