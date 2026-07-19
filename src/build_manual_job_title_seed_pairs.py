from pathlib import Path
import pandas as pd


SEED_PATH = Path("data/external_datasets/job_scraping/manual_job_title_seed.csv")
OUTPUT_PATH = Path("data/external_datasets/job_scraping/manual_scraped_style_job_title_bias_pairs.csv")
SUMMARY_PATH = Path("results/external_datasets/job_scraping/manual_scraped_style_job_title_summary.csv")
SUMMARY_MD = Path("docs/occupational_scope/manual_scraped_style_job_title_summary.md")


PAIR_MAP = [
    {
        "occupation_id": "manual_civil_engineer",
        "field": "Engineering",
        "occupation_key": "civil_engineer",
        "occupation_en": "civil engineer",
        "masculine_occupation": "مهندس مدني",
        "feminine_occupation": "مهندسة مدنية",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["مهندس مدني", "مهندسة مدنية"],
    },
    {
        "occupation_id": "manual_accountant",
        "field": "Business",
        "occupation_key": "accountant",
        "occupation_en": "accountant",
        "masculine_occupation": "محاسب",
        "feminine_occupation": "محاسبة",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["محاسب", "محاسبة"],
    },
    {
        "occupation_id": "manual_secretary",
        "field": "Administration",
        "occupation_key": "secretary",
        "occupation_en": "secretary",
        "masculine_occupation": "سكرتير",
        "feminine_occupation": "سكرتيرة",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["سكرتير", "سكرتيرة"],
    },
    {
        "occupation_id": "manual_pharmacist",
        "field": "Healthcare",
        "occupation_key": "pharmacist",
        "occupation_en": "pharmacist",
        "masculine_occupation": "صيدلي",
        "feminine_occupation": "صيدلانية",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["صيدلي", "صيدلانية"],
    },
    {
        "occupation_id": "manual_graphic_designer",
        "field": "Media_Creative",
        "occupation_key": "graphic_designer",
        "occupation_en": "graphic designer",
        "masculine_occupation": "مصمم جرافيك",
        "feminine_occupation": "مصممة جرافيك",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["مصمم جرافيك", "مصممة جرافيك"],
    },
    {
        "occupation_id": "manual_sales_representative",
        "field": "Business",
        "occupation_key": "sales_representative",
        "occupation_en": "sales representative",
        "masculine_occupation": "مندوب مبيعات",
        "feminine_occupation": "مندوبة مبيعات",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["مندوب مبيعات", "مندوبة مبيعات"],
    },
    {
        "occupation_id": "manual_driver",
        "field": "Services",
        "occupation_key": "driver",
        "occupation_en": "driver",
        "masculine_occupation": "سائق خاص",
        "feminine_occupation": "سائقة خاصة",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["سائق خاص", "سائقة خاصة"],
    },
    {
        "occupation_id": "manual_security_guard",
        "field": "Services",
        "occupation_key": "security_guard",
        "occupation_en": "security guard",
        "masculine_occupation": "فرد أمن",
        "feminine_occupation": "فردة أمن",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["فرد أمن", "فردة أمن"],
    },
    {
        "occupation_id": "manual_data_entry",
        "field": "Administration",
        "occupation_key": "data_entry",
        "occupation_en": "data entry clerk",
        "masculine_occupation": "مدخل بيانات",
        "feminine_occupation": "مدخلة بيانات",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["مدخل بيانات", "مدخلة بيانات"],
    },
    {
        "occupation_id": "manual_lawyer",
        "field": "Legal_Government",
        "occupation_key": "lawyer",
        "occupation_en": "lawyer",
        "masculine_occupation": "محامي",
        "feminine_occupation": "محامية",
        "stereotype_label": "unknown_manual_seed",
        "forms": ["محامي", "محامية"],
    },
]


def find_mapping(context):
    for mapping in PAIR_MAP:
        for form in mapping["forms"]:
            if form in context:
                return mapping, form

    return None, None


def main():
    if not SEED_PATH.exists():
        raise FileNotFoundError(f"Seed file not found: {SEED_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_MD.parent.mkdir(parents=True, exist_ok=True)

    seed_df = pd.read_csv(SEED_PATH, encoding="utf-8-sig")

    rows = []

    for idx, row in seed_df.iterrows():
        context = str(row["context_text"]).strip()

        mapping, matched_form = find_mapping(context)

        if mapping is None:
            continue

        masculine = mapping["masculine_occupation"]
        feminine = mapping["feminine_occupation"]

        if masculine in context:
            masculine_sentence = context
            feminine_sentence = context.replace(masculine, feminine, 1)
            original_gender = "masculine"
        elif feminine in context:
            feminine_sentence = context
            masculine_sentence = context.replace(feminine, masculine, 1)
            original_gender = "feminine"
        else:
            continue

        rows.append({
            "id": f"manual_scraped_style__{idx + 1:04d}",
            "benchmark_version": "manual_scraped_style_job_title_v1",
            "occupation_id": mapping["occupation_id"],
            "field": mapping["field"],
            "occupation_key": mapping["occupation_key"],
            "occupation_en": mapping["occupation_en"],
            "masculine_occupation": masculine,
            "feminine_occupation": feminine,
            "stereotype_label": mapping["stereotype_label"],
            "dialect": "Egyptian_or_MSA_job_board_style",
            "template_id": "manual_visible_job_title_seed",
            "template_type": "manual_scraped_style_context",
            "semantic_frame": "real_world_visible_job_title_context",
            "grammatical_gender_marker": "manual_seed_gendered_occupation",
            "source_id": row["source_id"],
            "source_name": row["source_name"],
            "source_type": row["source_type"],
            "source_url": row["source_url"],
            "original_context_text": context,
            "original_matched_gender": original_gender,
            "matched_form": matched_form,
            "match_source": "manual_visible_seed",
            "masculine_sentence": masculine_sentence,
            "feminine_sentence": feminine_sentence,
            "needs_manual_review": True,
            "review_reason": "manual visible seed; counterfactual form should be reviewed for agreement",
        })

    pairs_df = pd.DataFrame(rows)
    pairs_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    summary_df = pd.DataFrame([
        {"metric": "manual_seed_rows", "value": len(seed_df)},
        {"metric": "counterfactual_pairs", "value": len(pairs_df)},
        {"metric": "unique_occupations", "value": pairs_df["occupation_id"].nunique() if not pairs_df.empty else 0},
        {"metric": "unique_fields", "value": pairs_df["field"].nunique() if not pairs_df.empty else 0},
        {"metric": "manual_review_required", "value": True},
        {"metric": "status", "value": "completed_manual_seed"},
    ])

    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Manual Scraped-Style Job-Title Pilot Summary")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This pilot uses manually recorded visible job-title contexts from a public Arabic job page "
        "because automated scraping was disallowed by robots.txt."
    )
    md.append("")
    md.append("## Ethical Note")
    md.append("")
    md.append(
        "The automated scraper respected robots.txt and did not fetch disallowed pages. "
        "This manual seed is used only as a small external enrichment pilot."
    )
    md.append("")
    md.append("## Summary")
    md.append("")
    for _, item in summary_df.iterrows():
        md.append(f"- {item['metric']}: {item['value']}")
    md.append("")
    md.append("## Contribution")
    md.append("")
    md.append(
        "This adds a real-world visible job-title context pilot without violating website scraping restrictions."
    )
    md.append("")

    SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")

    print("Manual scraped-style job-title pairs created.")
    print("Pairs:", OUTPUT_PATH)
    print("Summary:", SUMMARY_PATH)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()