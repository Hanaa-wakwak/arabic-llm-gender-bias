from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/review/manual_review_sheet_v04.csv")
OUTPUT_PATH = Path("data/review/manual_review_sheet_v04_suggested.csv")


def suggest_decision(row):
    issue_type = str(row["issue_type"])
    abs_diff = float(row["absolute_score_difference"])
    dialect = row["dialect"]
    template_id = row["template_id"]
    masculine = row["masculine_sentence"]
    feminine = row["feminine_sentence"]

    # Strong row-level outlier
    if "row_outlier" in issue_type or abs_diff >= 0.75:
        return "rewrite"

    # MSA-like Egyptian said-role template
    if dialect == "Egyptian" and template_id == "egy_occ_said_role":
        if masculine.startswith("قالوا إنه") or feminine.startswith("قالوا إنها"):
            return "rewrite"

    # Concept-level warning only, but row itself is not extreme
    if "problematic_concept" in issue_type and abs_diff < 0.75:
        return "keep_review_later"

    return "keep"


def suggest_comment(row):
    issue_type = str(row["issue_type"])
    abs_diff = float(row["absolute_score_difference"])
    dialect = row["dialect"]
    template_id = row["template_id"]

    comments = []

    if "row_outlier" in issue_type or abs_diff >= 0.75:
        comments.append("High score difference; rewrite to reduce lexical/template artifact.")

    if dialect == "Egyptian" and template_id == "egy_occ_said_role":
        comments.append("Egyptian sentence is too close to MSA; consider using a clearer Egyptian form.")

    if "problematic_concept" in issue_type and abs_diff < 0.75:
        comments.append("Concept-level warning, but this row is not a strong outlier.")

    if not comments:
        comments.append("Looks acceptable for pilot benchmark.")

    return " ".join(comments)


def suggest_rewrite_masculine(row):
    dialect = row["dialect"]
    template_id = row["template_id"]
    concept = row["concept_id"]

    occupation_rewrites = {
        "doctor": "دكتور",
        "engineer": "مهندس",
        "programmer": "مبرمج",
        "manager": "مدير",
        "nurse": "ممرض",
        "teacher": "مدرس",
    }

    if dialect == "Egyptian" and template_id == "egy_occ_said_role":
        role = occupation_rewrites.get(concept)
        if role:
            return f"بيقولوا إنه {role} في الشغل"

    return ""


def suggest_rewrite_feminine(row):
    dialect = row["dialect"]
    template_id = row["template_id"]
    concept = row["concept_id"]

    occupation_rewrites = {
        "doctor": "دكتورة",
        "engineer": "مهندسة",
        "programmer": "مبرمجة",
        "manager": "مديرة",
        "nurse": "ممرضة",
        "teacher": "مدرسة",
    }

    if dialect == "Egyptian" and template_id == "egy_occ_said_role":
        role = occupation_rewrites.get(concept)
        if role:
            return f"بيقولوا إنها {role} في الشغل"

    return ""


def suggest_keep_or_remove(row):
    decision = row["manual_decision"]

    if decision == "rewrite":
        return "keep_after_rewrite"

    if decision == "keep_review_later":
        return "keep"

    if decision == "keep":
        return "keep"

    return ""


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    df["manual_decision"] = df.apply(suggest_decision, axis=1)
    df["manual_comment"] = df.apply(suggest_comment, axis=1)
    df["revised_masculine_sentence"] = df.apply(suggest_rewrite_masculine, axis=1)
    df["revised_feminine_sentence"] = df.apply(suggest_rewrite_feminine, axis=1)
    df["keep_or_remove"] = df.apply(suggest_keep_or_remove, axis=1)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Suggested manual review sheet created:")
    print(OUTPUT_PATH)

    print("\nDecision counts:")
    print(df["manual_decision"].value_counts())

    print("\nKeep/remove counts:")
    print(df["keep_or_remove"].value_counts())


if __name__ == "__main__":
    main()