from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/review/manual_review_sheet_v04_suggested.csv")
OUTPUT_PATH = Path("data/review/manual_review_missing_rewrites_v04.csv")


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    rewrite_df = df[df["manual_decision"] == "rewrite"].copy()

    missing_rewrites = rewrite_df[
        (rewrite_df["revised_masculine_sentence"].isna() | (rewrite_df["revised_masculine_sentence"].astype(str).str.strip() == ""))
        | (rewrite_df["revised_feminine_sentence"].isna() | (rewrite_df["revised_feminine_sentence"].astype(str).str.strip() == ""))
    ].copy()

    missing_rewrites.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("=" * 70)
    print("Manual Review Sheet Validation")
    print("=" * 70)

    print("\nTotal review rows:")
    print(len(df))

    print("\nDecision counts:")
    print(df["manual_decision"].value_counts())

    print("\nRewrite rows:")
    print(len(rewrite_df))

    print("\nRewrite rows with missing revised sentences:")
    print(len(missing_rewrites))

    print("\nMissing rewrite rows saved to:")
    print(OUTPUT_PATH)

    if len(missing_rewrites) > 0:
        print("\nRows needing revised sentences:")
        print(
            missing_rewrites[
                [
                    "id",
                    "concept_id",
                    "dimension",
                    "dialect",
                    "template_id",
                    "masculine_sentence",
                    "feminine_sentence",
                    "score_difference",
                    "issue_type",
                ]
            ]
        )
    else:
        print("\nAll rewrite rows have revised sentences. Ready to build v0.5.")


if __name__ == "__main__":
    main()