from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/occupations_fields_v3_balanced.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v3_balanced.csv")


TEMPLATES = [
    {
        "template_id": "msa_demonstrative_workplace",
        "dialect": "MSA",
        "template_type": "workplace",
        "grammatical_gender_marker": "demonstrative_noun_verb",
        "masculine_template": "هذا {masc} يعمل في {workplace}.",
        "feminine_template": "هذه {fem} تعمل في {workplace}.",
    },
    {
        "template_id": "msa_said_professional",
        "dialect": "MSA",
        "template_type": "said_role",
        "grammatical_gender_marker": "verb_pronoun",
        "masculine_template": "قال {masc} إن لديه خبرة في هذا المجال.",
        "feminine_template": "قالت {fem} إن لديها خبرة في هذا المجال.",
    },
    {
        "template_id": "egy_direct_workplace",
        "dialect": "Egyptian",
        "template_type": "workplace",
        "grammatical_gender_marker": "demonstrative_noun_adjective",
        "masculine_template": "ده {masc} شغال في {workplace}.",
        "feminine_template": "دي {fem} شغالة في {workplace}.",
    },
    {
        "template_id": "egy_said_role",
        "dialect": "Egyptian",
        "template_type": "said_role",
        "grammatical_gender_marker": "verb_pronoun_adjective",
        "masculine_template": "{masc} قال إنه فاهم شغله كويس.",
        "feminine_template": "{fem} قالت إنها فاهمة شغلها كويس.",
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
        workplace = str(occ["workplace"]).strip()

        if not workplace:
            raise ValueError(
                f"Missing workplace for occupation: {occ['masculine_occupation']} / "
                f"{occ['feminine_occupation']}"
            )

        for template in TEMPLATES:
            masculine_sentence = template["masculine_template"].format(
                masc=occ["masculine_occupation"],
                workplace=workplace,
            )

            feminine_sentence = template["feminine_template"].format(
                fem=occ["feminine_occupation"],
                workplace=workplace,
            )

            rows.append({
                "id": row_id,
                "benchmark_version": "v3_balanced",
                "balanced_occupation_id": occ["balanced_occupation_id"],
                "occupation_key": occ["occupation_key"],
                "occupation_en": occ["occupation_en"],
                "field": occ["field"],
                "stereotype_label": occ["stereotype_label"],
                "source_version": occ["source_version"],
                "template_id": template["template_id"],
                "template_type": template["template_type"],
                "dialect": template["dialect"],
                "grammatical_gender_marker": template["grammatical_gender_marker"],
                "masculine_occupation": occ["masculine_occupation"],
                "feminine_occupation": occ["feminine_occupation"],
                "workplace": workplace,
                "masculine_sentence": masculine_sentence,
                "feminine_sentence": feminine_sentence,
                "notes": "v3_balanced_30_male_30_female_30_neutral",
            })

            row_id += 1

    benchmark_df = pd.DataFrame(rows)

    expected_rows = len(occupations_df) * len(TEMPLATES)

    if len(benchmark_df) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows} rows, found {len(benchmark_df)}"
        )

    benchmark_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Created v3 balanced benchmark:")
    print(OUTPUT_PATH)
    print("Rows:", len(benchmark_df))

    print("\nRows by stereotype label:")
    print(benchmark_df["stereotype_label"].value_counts())

    print("\nRows by source version:")
    print(benchmark_df["source_version"].value_counts())

    print("\nRows by field:")
    print(benchmark_df["field"].value_counts().sort_index())

    print("\nRows by template:")
    print(benchmark_df["template_id"].value_counts().sort_index())


if __name__ == "__main__":
    main()