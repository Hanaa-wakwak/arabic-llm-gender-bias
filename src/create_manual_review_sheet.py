from pathlib import Path
import pandas as pd


RESULTS_DIR = Path("results")
OUTPUT_DIR = Path("data/review")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCORING_PATH = RESULTS_DIR / "scoring_results_v04.csv"
QUALITY_CONCEPT_PATH = RESULTS_DIR / "quality_by_concept_id_v04.csv"
QUALITY_TEMPLATE_PATH = RESULTS_DIR / "quality_by_template_id_v04.csv"

OUTPUT_PATH = OUTPUT_DIR / "manual_review_sheet_v04.csv"


def main():
    scoring_df = pd.read_csv(SCORING_PATH, encoding="utf-8-sig")
    concept_quality = pd.read_csv(QUALITY_CONCEPT_PATH, encoding="utf-8-sig")
    template_quality = pd.read_csv(QUALITY_TEMPLATE_PATH, encoding="utf-8-sig")

    problematic_concepts = concept_quality[
        concept_quality["warnings"] != "ok"
    ]["concept_id"].tolist()

    problematic_templates = template_quality[
        template_quality["warnings"] != "ok"
    ]["template_id"].tolist()

    scoring_df["absolute_score_difference"] = scoring_df["score_difference"].abs()

    review_df = scoring_df[
        (scoring_df["concept_id"].isin(problematic_concepts))
        | (scoring_df["template_id"].isin(problematic_templates))
        | (scoring_df["absolute_score_difference"] >= 0.75)
    ].copy()

    def issue_type(row):
        issues = []

        if row["concept_id"] in problematic_concepts:
            issues.append("problematic_concept")

        if row["template_id"] in problematic_templates:
            issues.append("problematic_template")

        if row["absolute_score_difference"] >= 0.75:
            issues.append("row_outlier")

        return ";".join(issues)

    review_df["issue_type"] = review_df.apply(issue_type, axis=1)

    review_df["manual_decision"] = ""
    review_df["manual_comment"] = ""
    review_df["revised_masculine_sentence"] = ""
    review_df["revised_feminine_sentence"] = ""
    review_df["keep_or_remove"] = ""

    columns = [
        "id",
        "concept_id",
        "dimension",
        "dialect",
        "template_id",
        "stereotype_direction",
        "masculine_sentence",
        "feminine_sentence",
        "masculine_score",
        "feminine_score",
        "score_difference",
        "absolute_score_difference",
        "preferred_gender",
        "issue_type",
        "manual_decision",
        "manual_comment",
        "revised_masculine_sentence",
        "revised_feminine_sentence",
        "keep_or_remove",
    ]

    review_df = review_df[columns]
    review_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Manual review sheet created:")
    print(OUTPUT_PATH)

    print("\nRows selected for manual review:")
    print(len(review_df))

    print("\nIssue type counts:")
    print(review_df["issue_type"].value_counts())


if __name__ == "__main__":
    main()