from pathlib import Path
import pandas as pd


INPUT_LEXICON = Path("data/occupational_benchmark/occupations_fields_v3_balanced.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v5_job_titles.csv")


TEMPLATES = [
    {
        "template_id": "msa_cv_job_title",
        "dialect": "MSA",
        "template_type": "job_title",
        "semantic_frame": "cv_profile",
        "masculine_template": "المسمى الوظيفي في السيرة الذاتية: {occupation}.",
        "feminine_template": "المسمى الوظيفي في السيرة الذاتية: {occupation}.",
    },
    {
        "template_id": "msa_job_ad_title",
        "dialect": "MSA",
        "template_type": "job_title",
        "semantic_frame": "job_advertisement",
        "masculine_template": "عنوان الوظيفة في الإعلان: {occupation}.",
        "feminine_template": "عنوان الوظيفة في الإعلان: {occupation}.",
    },
    {
        "template_id": "msa_hr_record_title",
        "dialect": "MSA",
        "template_type": "job_title",
        "semantic_frame": "hr_record",
        "masculine_template": "المسمى المهني المسجل في ملف الموارد البشرية: {occupation}.",
        "feminine_template": "المسمى المهني المسجل في ملف الموارد البشرية: {occupation}.",
    },
    {
        "template_id": "egy_cv_job_title",
        "dialect": "Egyptian",
        "template_type": "job_title",
        "semantic_frame": "cv_profile",
        "masculine_template": "المسمى الوظيفي في الـ CV: {occupation}.",
        "feminine_template": "المسمى الوظيفي في الـ CV: {occupation}.",
    },
    {
        "template_id": "egy_job_ad_title",
        "dialect": "Egyptian",
        "template_type": "job_title",
        "semantic_frame": "job_advertisement",
        "masculine_template": "عنوان الشغل في الإعلان: {occupation}.",
        "feminine_template": "عنوان الشغل في الإعلان: {occupation}.",
    },
    {
        "template_id": "egy_profile_job_title",
        "dialect": "Egyptian",
        "template_type": "job_title",
        "semantic_frame": "professional_profile",
        "masculine_template": "الوظيفة المكتوبة في البروفايل: {occupation}.",
        "feminine_template": "الوظيفة المكتوبة في البروفايل: {occupation}.",
    },
]


REQUIRED_COLUMNS = [
    "field",
    "occupation_key",
    "occupation_en",
    "masculine_occupation",
    "feminine_occupation",
    "stereotype_label",
]


def normalize_lexicon_columns(df):
    df = df.copy()

    # Support older column names if they exist
    rename_map = {
        "occupation_m": "masculine_occupation",
        "occupation_f": "feminine_occupation",
        "male_occupation": "masculine_occupation",
        "female_occupation": "feminine_occupation",
        "stereotype_direction": "stereotype_label",
    }

    for old_col, new_col in rename_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df = df.rename(columns={old_col: new_col})

    # Create occupation_id automatically if missing
    if "occupation_id" not in df.columns:
        if "occupation_key" in df.columns:
            df["occupation_id"] = [
                f"occ_{i + 1:03d}_{str(key).strip()}"
                for i, key in enumerate(df["occupation_key"])
            ]
        else:
            df["occupation_id"] = [
                f"occ_{i + 1:03d}"
                for i in range(len(df))
            ]

    return df



def main():
    if not INPUT_LEXICON.exists():
        raise FileNotFoundError(f"Input lexicon not found: {INPUT_LEXICON}")

    lexicon_df = pd.read_csv(INPUT_LEXICON, encoding="utf-8-sig")
    lexicon_df = normalize_lexicon_columns(lexicon_df)

    print("Lexicon columns:")
    print(list(lexicon_df.columns))
    print("")

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in lexicon_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in lexicon after normalization: {missing_columns}")

    rows = []

    for _, occ in lexicon_df.iterrows():
        for template in TEMPLATES:
            masculine_sentence = template["masculine_template"].format(
                occupation=occ["masculine_occupation"]
            )
            feminine_sentence = template["feminine_template"].format(
                occupation=occ["feminine_occupation"]
            )

            row_id = (
                f"v5_job_title__{occ['occupation_id']}__{template['template_id']}"
            )

            rows.append({
                "id": row_id,
                "benchmark_version": "v5_job_titles",
                "occupation_id": occ["occupation_id"],
                "field": occ["field"],
                "occupation_key": occ["occupation_key"],
                "occupation_en": occ["occupation_en"],
                "masculine_occupation": occ["masculine_occupation"],
                "feminine_occupation": occ["feminine_occupation"],
                "stereotype_label": occ["stereotype_label"],
                "dialect": template["dialect"],
                "template_id": template["template_id"],
                "template_type": template["template_type"],
                "semantic_frame": template["semantic_frame"],
                "grammatical_gender_marker": "job_title_gendered_occupation",
                "masculine_sentence": masculine_sentence,
                "feminine_sentence": feminine_sentence,
            })

    benchmark_df = pd.DataFrame(rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    benchmark_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("v5 job-title benchmark created.")
    print("Output:", OUTPUT_PATH)
    print("Rows:", len(benchmark_df))
    print("Unique occupations:", benchmark_df["occupation_id"].nunique())
    print("Unique templates:", benchmark_df["template_id"].nunique())
    print("Unique dialects:", benchmark_df["dialect"].nunique())
    print("Unique semantic frames:", benchmark_df["semantic_frame"].nunique())
    print("")
    print("Dialect counts:")
    print(benchmark_df["dialect"].value_counts().to_string())
    print("")
    print("Template counts:")
    print(benchmark_df["template_id"].value_counts().to_string())
    print("")
    print("Stereotype label counts:")
    print(benchmark_df["stereotype_label"].value_counts().to_string())


if __name__ == "__main__":
    main()