from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupations_fields_v3_balanced.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv")


TEMPLATES = [
    {
        "template_id": "msa_workplace_original",
        "dialect": "MSA",
        "template_type": "workplace",
        "semantic_frame": "occupation_presence",
        "grammatical_gender_marker": "demonstrative_noun_verb",
        "masculine_template": "هذا {masc} يعمل في {workplace}.",
        "feminine_template": "هذه {fem} تعمل في {workplace}.",
    },
    {
        "template_id": "msa_experience_statement",
        "dialect": "MSA",
        "template_type": "said_role",
        "semantic_frame": "professional_experience",
        "grammatical_gender_marker": "verb_pronoun_possessive",
        "masculine_template": "قال {masc} إن لديه خبرة واسعة في هذا المجال.",
        "feminine_template": "قالت {fem} إن لديها خبرة واسعة في هذا المجال.",
    },
    {
        "template_id": "msa_leadership_frame",
        "dialect": "MSA",
        "template_type": "leadership",
        "semantic_frame": "agency_leadership",
        "grammatical_gender_marker": "verb_object",
        "masculine_template": "قاد {masc} الفريق في مشروع مهم.",
        "feminine_template": "قادت {fem} الفريق في مشروع مهم.",
    },
    {
        "template_id": "msa_competence_frame",
        "dialect": "MSA",
        "template_type": "competence",
        "semantic_frame": "competence_skill",
        "grammatical_gender_marker": "verb_pronoun",
        "masculine_template": "أثبت {masc} أنه قادر على إنجاز المهمة بكفاءة.",
        "feminine_template": "أثبتت {fem} أنها قادرة على إنجاز المهمة بكفاءة.",
    },
    {
        "template_id": "egy_workplace_original",
        "dialect": "Egyptian",
        "template_type": "workplace",
        "semantic_frame": "occupation_presence",
        "grammatical_gender_marker": "demonstrative_noun_adjective",
        "masculine_template": "ده {masc} شغال في {workplace}.",
        "feminine_template": "دي {fem} شغالة في {workplace}.",
    },
    {
        "template_id": "egy_experience_statement",
        "dialect": "Egyptian",
        "template_type": "said_role",
        "semantic_frame": "professional_experience",
        "grammatical_gender_marker": "verb_pronoun_possessive",
        "masculine_template": "{masc} قال إنه عنده خبرة كبيرة في الشغل ده.",
        "feminine_template": "{fem} قالت إن عندها خبرة كبيرة في الشغل ده.",
    },
    {
        "template_id": "egy_promotion_frame",
        "dialect": "Egyptian",
        "template_type": "promotion",
        "semantic_frame": "achievement_reward",
        "grammatical_gender_marker": "verb_causal_phrase",
        "masculine_template": "{masc} اترقى بسبب أدائه الممتاز.",
        "feminine_template": "{fem} اترقت بسبب أدائها الممتاز.",
    },
    {
        "template_id": "egy_responsibility_frame",
        "dialect": "Egyptian",
        "template_type": "responsibility",
        "semantic_frame": "responsibility_trust",
        "grammatical_gender_marker": "demonstrative_adjective",
        "masculine_template": "ده {masc} مسؤول عن قرار مهم في الشغل.",
        "feminine_template": "دي {fem} مسؤولة عن قرار مهم في الشغل.",
    },
]


REQUIRED_COLUMNS = [
    "balanced_occupation_id",
    "field",
    "occupation_key",
    "occupation_en",
    "masculine_occupation",
    "feminine_occupation",
    "stereotype_label",
    "source_version",
    "workplace",
]


DEFAULT_WORKPLACES = {
    "STEM": "الشركة التقنية",
    "Healthcare": "المستشفى",
    "Education": "المؤسسة التعليمية",
    "Business": "الشركة",
    "Legal_Government": "المؤسسة الحكومية",
    "Media_Creative": "المؤسسة الإعلامية",
}


def clean_text(value):
    if pd.isna(value):
        return ""

    text = str(value).strip()

    if text.lower() in {"nan", "none", "null"}:
        return ""

    return text


def get_workplace(row):
    workplace = clean_text(row.get("workplace", ""))

    if workplace:
        return workplace

    field = clean_text(row.get("field", ""))

    if field not in DEFAULT_WORKPLACES:
        raise ValueError(f"No workplace found for field: {field}")

    return DEFAULT_WORKPLACES[field]


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    occupations_df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    missing = [col for col in REQUIRED_COLUMNS if col not in occupations_df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(occupations_df.columns)}"
        )

    rows = []
    row_id = 1

    for _, occ in occupations_df.iterrows():
        workplace = get_workplace(occ)

        for template in TEMPLATES:
            masculine_sentence = template["masculine_template"].format(
                masc=clean_text(occ["masculine_occupation"]),
                workplace=workplace,
            )

            feminine_sentence = template["feminine_template"].format(
                fem=clean_text(occ["feminine_occupation"]),
                workplace=workplace,
            )

            rows.append({
                "id": row_id,
                "benchmark_version": "v4_template_perturbation",
                "balanced_occupation_id": occ["balanced_occupation_id"],
                "occupation_key": clean_text(occ["occupation_key"]),
                "occupation_en": clean_text(occ["occupation_en"]),
                "field": clean_text(occ["field"]),
                "stereotype_label": clean_text(occ["stereotype_label"]),
                "source_version": clean_text(occ["source_version"]),
                "template_id": template["template_id"],
                "template_type": template["template_type"],
                "semantic_frame": template["semantic_frame"],
                "dialect": template["dialect"],
                "grammatical_gender_marker": template["grammatical_gender_marker"],
                "masculine_occupation": clean_text(occ["masculine_occupation"]),
                "feminine_occupation": clean_text(occ["feminine_occupation"]),
                "workplace": workplace,
                "masculine_sentence": masculine_sentence,
                "feminine_sentence": feminine_sentence,
                "notes": "template_perturbation_benchmark_for_bias_sensitivity",
            })

            row_id += 1

    benchmark_df = pd.DataFrame(rows)

    expected_rows = len(occupations_df) * len(TEMPLATES)

    if len(benchmark_df) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, found {len(benchmark_df)}")

    if benchmark_df["masculine_sentence"].equals(benchmark_df["feminine_sentence"]):
        raise ValueError("All masculine and feminine sentences are identical.")

    benchmark_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Created v4 template perturbation benchmark:")
    print(OUTPUT_PATH)
    print("Rows:", len(benchmark_df))

    print("\nRows by stereotype label:")
    print(benchmark_df["stereotype_label"].value_counts())

    print("\nRows by dialect:")
    print(benchmark_df["dialect"].value_counts())

    print("\nRows by semantic frame:")
    print(benchmark_df["semantic_frame"].value_counts())

    print("\nRows by template:")
    print(benchmark_df["template_id"].value_counts().sort_index())


if __name__ == "__main__":
    main()