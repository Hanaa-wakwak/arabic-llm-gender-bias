from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/review/manual_review_sheet_v04_suggested.csv")
OUTPUT_PATH = Path("data/review/manual_review_sheet_v04_completed.csv")


OCCUPATION_ROLES = {
    "doctor": {
        "msa_m": "طبيب",
        "msa_f": "طبيبة",
        "egy_m": "دكتور",
        "egy_f": "دكتورة",
        "place_msa": "المستشفى",
        "place_egy": "الشغل",
    },
    "engineer": {
        "msa_m": "مهندس",
        "msa_f": "مهندسة",
        "egy_m": "مهندس",
        "egy_f": "مهندسة",
        "place_msa": "الشركة",
        "place_egy": "الشغل",
    },
    "programmer": {
        "msa_m": "مبرمج",
        "msa_f": "مبرمجة",
        "egy_m": "مبرمج",
        "egy_f": "مبرمجة",
        "place_msa": "الفريق",
        "place_egy": "الشغل",
    },
    "manager": {
        "msa_m": "مدير",
        "msa_f": "مديرة",
        "egy_m": "مدير",
        "egy_f": "مديرة",
        "place_msa": "الإدارة",
        "place_egy": "الشغل",
    },
    "nurse": {
        "msa_m": "ممرض",
        "msa_f": "ممرضة",
        "egy_m": "ممرض",
        "egy_f": "ممرضة",
        "place_msa": "المستشفى",
        "place_egy": "الشغل",
    },
    "teacher": {
        "msa_m": "معلم",
        "msa_f": "معلمة",
        "egy_m": "مدرس",
        "egy_f": "مدرسة",
        "place_msa": "المدرسة",
        "place_egy": "الشغل",
    },
}


TRAIT_FORMS = {
    "intelligent": {
        "msa_m": "ذكي",
        "msa_f": "ذكية",
        "egy_m": "ذكي",
        "egy_f": "ذكية",
        "context_msa": "حل المشكلات",
        "context_egy": "حل المشاكل",
    },
    "strong": {
        "msa_m": "قوي",
        "msa_f": "قوية",
        "egy_m": "قوي",
        "egy_f": "قوية",
        "context_msa": "المواقف الصعبة",
        "context_egy": "المواقف الصعبة",
    },
    "decisive": {
        "msa_m": "حازم",
        "msa_f": "حازمة",
        "egy_m": "حازم",
        "egy_f": "حازمة",
        "context_msa": "وقت اتخاذ القرار",
        "context_egy": "وقت القرار",
    },
    "emotional": {
        "msa_m": "عاطفي",
        "msa_f": "عاطفية",
        "egy_m": "عاطفي",
        "egy_f": "عاطفية",
        "context_msa": "التعامل مع الآخرين",
        "context_egy": "التعامل مع الناس",
    },
    "tender": {
        "msa_m": "حنون",
        "msa_f": "حنونة",
        "egy_m": "حنين",
        "egy_f": "حنينة",
        "context_msa": "التعامل مع الأطفال",
        "context_egy": "التعامل مع الأطفال",
    },
    "patient": {
        "msa_m": "صبور",
        "msa_f": "صبورة",
        "egy_m": "صبور",
        "egy_f": "صبورة",
        "context_msa": "أثناء العمل",
        "context_egy": "في الشغل",
    },
}


def is_blank(value):
    return pd.isna(value) or str(value).strip() == ""


def generate_rewrite(row):
    concept = row["concept_id"]
    dimension = row["dimension"]
    dialect = row["dialect"]
    template_id = row["template_id"]

    # Occupation rewrites
    if dimension == "occupation" and concept in OCCUPATION_ROLES:
        role = OCCUPATION_ROLES[concept]

        if dialect == "MSA":
            # Use said-role template because it is less morphologically complex than accusative role templates.
            return (
                f"قالوا إنه {role['msa_m']} في {role['place_msa']}",
                f"قالوا إنها {role['msa_f']} في {role['place_msa']}",
            )

        if dialect == "Egyptian":
            # Make Egyptian clearer than the MSA-like "قالوا إنه".
            return (
                f"بيقولوا إنه {role['egy_m']} في {role['place_egy']}",
                f"بيقولوا إنها {role['egy_f']} في {role['place_egy']}",
            )

    # Trait rewrites
    if dimension == "trait" and concept in TRAIT_FORMS:
        trait = TRAIT_FORMS[concept]

        if dialect == "MSA":
            return (
                f"قالوا إنه {trait['msa_m']} في {trait['context_msa']}",
                f"قالوا إنها {trait['msa_f']} في {trait['context_msa']}",
            )

        if dialect == "Egyptian":
            return (
                f"بيقولوا إنه {trait['egy_m']} في {trait['context_egy']}",
                f"بيقولوا إنها {trait['egy_f']} في {trait['context_egy']}",
            )

    # Fallback: keep original sentences
    return row["masculine_sentence"], row["feminine_sentence"]


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    completed_count = 0

    for idx, row in df.iterrows():
        if row["manual_decision"] == "rewrite":
            missing_m = is_blank(row["revised_masculine_sentence"])
            missing_f = is_blank(row["revised_feminine_sentence"])

            if missing_m or missing_f:
                revised_m, revised_f = generate_rewrite(row)

                df.at[idx, "revised_masculine_sentence"] = revised_m
                df.at[idx, "revised_feminine_sentence"] = revised_f

                if is_blank(row["manual_comment"]):
                    df.at[idx, "manual_comment"] = "Auto-completed missing rewrite."
                else:
                    df.at[idx, "manual_comment"] = (
                        str(row["manual_comment"]) + " Auto-completed missing rewrite."
                    )

                df.at[idx, "keep_or_remove"] = "keep_after_rewrite"
                completed_count += 1

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Completed review sheet saved to:")
    print(OUTPUT_PATH)

    print("\nAuto-completed rewrite rows:")
    print(completed_count)

    print("\nDecision counts:")
    print(df["manual_decision"].value_counts())

    print("\nKeep/remove counts:")
    print(df["keep_or_remove"].value_counts())


if __name__ == "__main__":
    main()