from pathlib import Path
import re
import pandas as pd


ARABJOBS_PATH = Path("data/external_datasets/arabjobs/ArabJobs.csv")
V6_LEXICON_PATH = Path("data/occupational_benchmark/job_roles_expanded_lexicon_v6.csv")

OUTPUT_DIR = Path("data/external_datasets/arabjobs")
RESULTS_DIR = Path("results/external_datasets/arabjobs")
DOC_PATH = Path("docs/occupational_scope/arabjobs_v7_external_dataset_summary.md")

OUTPUT_PAIRS = OUTPUT_DIR / "arabjobs_v7_counterfactual_pairs.csv"
MATCHED_ROWS = OUTPUT_DIR / "arabjobs_v7_matched_rows.csv"
UNMATCHED_ROWS = OUTPUT_DIR / "arabjobs_v7_unmatched_rows_sample.csv"
SUMMARY_PATH = RESULTS_DIR / "arabjobs_v7_preparation_summary.csv"


TEMPLATES = [
    {
        "template_id": "arabjobs_v7_job_title_record",
        "template_type": "job_title_record",
        "semantic_frame": "real_world_job_title",
        "dialect": "Mixed_Arabic",
        "masculine": "المسمى الوظيفي في الإعلان هو {masculine_title}.",
        "feminine": "المسمى الوظيفي في الإعلان هو {feminine_title}.",
    },
    {
        "template_id": "arabjobs_v7_country_job_context",
        "template_type": "country_job_context",
        "semantic_frame": "country_labor_market",
        "dialect": "Mixed_Arabic",
        "masculine": "في سوق العمل في {country}، يظهر إعلان لوظيفة {masculine_title}.",
        "feminine": "في سوق العمل في {country}، يظهر إعلان لوظيفة {feminine_title}.",
    },
    {
        "template_id": "arabjobs_v7_category_context",
        "template_type": "category_context",
        "semantic_frame": "job_category",
        "dialect": "Mixed_Arabic",
        "masculine": "ضمن فئة {job_category}، يظهر المسمى الوظيفي {masculine_title}.",
        "feminine": "ضمن فئة {job_category}، يظهر المسمى الوظيفي {feminine_title}.",
    },
    {
        "template_id": "arabjobs_v7_profession_context",
        "template_type": "profession_context",
        "semantic_frame": "profession_listing",
        "dialect": "Mixed_Arabic",
        "masculine": "يرتبط الإعلان بمهنة {profession} ويذكر وظيفة {masculine_title}.",
        "feminine": "يرتبط الإعلان بمهنة {profession} ويذكر وظيفة {feminine_title}.",
    },
    {
        "template_id": "arabjobs_v7_recruitment_context",
        "template_type": "recruitment_context",
        "semantic_frame": "hiring_language",
        "dialect": "Mixed_Arabic",
        "masculine": "تبحث جهة العمل عن {masculine_title} مناسب لهذه الوظيفة.",
        "feminine": "تبحث جهة العمل عن {feminine_title} مناسبة لهذه الوظيفة.",
    },
    {
        "template_id": "arabjobs_v7_application_context",
        "template_type": "application_context",
        "semantic_frame": "candidate_application",
        "dialect": "Mixed_Arabic",
        "masculine": "تقدم {masculine_title} إلى هذا الإعلان بعد قراءة تفاصيل الوظيفة.",
        "feminine": "تقدمت {feminine_title} إلى هذا الإعلان بعد قراءة تفاصيل الوظيفة.",
    },
]


def normalize_text(value):
    if pd.isna(value):
        return ""
    text = str(value)
    text = text.replace("\u200f", " ").replace("\u200e", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def safe_value(row, col, default="unknown"):
    value = row.get(col, default)
    value = normalize_text(value)
    return value if value else default


def detect_match(row, lexicon):
    searchable = " ".join([
        safe_value(row, "job_title", ""),
        safe_value(row, "profession", ""),
        safe_value(row, "description", ""),
    ])

    matches = []

    for _, role in lexicon.iterrows():
        masculine = normalize_text(role["masculine_job_title"])
        feminine = normalize_text(role["feminine_job_title"])

        masculine_found = masculine and masculine in searchable
        feminine_found = feminine and feminine in searchable

        if masculine_found or feminine_found:
            matches.append({
                "role_id": role["role_id"],
                "department": role["department"],
                "job_family": role["job_family"],
                "role_key": role["role_key"],
                "seniority_level": role["seniority_level"],
                "job_role_type": role["job_role_type"],
                "masculine_job_title": masculine,
                "feminine_job_title": feminine,
                "matched_form": "both" if masculine_found and feminine_found else ("masculine" if masculine_found else "feminine"),
            })

    if not matches:
        return None

    matches = sorted(matches, key=lambda x: len(x["masculine_job_title"]) + len(x["feminine_job_title"]), reverse=True)
    return matches[0]


def main():
    if not ARABJOBS_PATH.exists():
        raise FileNotFoundError(f"Missing ArabJobs CSV: {ARABJOBS_PATH}")

    if not V6_LEXICON_PATH.exists():
        raise FileNotFoundError(f"Missing v6 lexicon: {V6_LEXICON_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    arabjobs = pd.read_csv(ARABJOBS_PATH, encoding="utf-8-sig")
    lexicon = pd.read_csv(V6_LEXICON_PATH, encoding="utf-8-sig")

    required_arabjobs_cols = [
        "job_title",
        "profession",
        "description",
        "gender",
        "country",
        "job_category",
        "sub_category",
    ]

    missing_cols = [c for c in required_arabjobs_cols if c not in arabjobs.columns]
    if missing_cols:
        raise ValueError(f"Missing expected ArabJobs columns: {missing_cols}")

    matched_rows = []
    unmatched_rows = []
    pair_rows = []

    pair_index = 1

    for idx, row in arabjobs.iterrows():
        match = detect_match(row, lexicon)

        if match is None:
            unmatched_rows.append({
                "arabjobs_row_id": idx,
                "job_title": safe_value(row, "job_title"),
                "profession": safe_value(row, "profession"),
                "gender": safe_value(row, "gender"),
                "country": safe_value(row, "country"),
                "job_category": safe_value(row, "job_category"),
                "sub_category": safe_value(row, "sub_category"),
            })
            continue

        matched_record = {
            "arabjobs_row_id": idx,
            "job_title": safe_value(row, "job_title"),
            "profession": safe_value(row, "profession"),
            "description": safe_value(row, "description"),
            "gender": safe_value(row, "gender"),
            "country": safe_value(row, "country"),
            "job_category": safe_value(row, "job_category"),
            "sub_category": safe_value(row, "sub_category"),
            **match,
        }

        matched_rows.append(matched_record)

        for template in TEMPLATES:
            masculine_sentence = template["masculine"].format(
                masculine_title=match["masculine_job_title"],
                feminine_title=match["feminine_job_title"],
                country=safe_value(row, "country"),
                job_category=safe_value(row, "job_category"),
                sub_category=safe_value(row, "sub_category"),
                profession=safe_value(row, "profession"),
            )

            feminine_sentence = template["feminine"].format(
                masculine_title=match["masculine_job_title"],
                feminine_title=match["feminine_job_title"],
                country=safe_value(row, "country"),
                job_category=safe_value(row, "job_category"),
                sub_category=safe_value(row, "sub_category"),
                profession=safe_value(row, "profession"),
            )

            pair_rows.append({
                "id": f"arabjobs_v7_pair_{pair_index:06d}",
                "benchmark_version": "arabjobs_v7_external_real_world_job_ads",
                "external_dataset": "ArabJobs",
                "arabjobs_row_id": idx,

                "field": match["department"],
                "department": match["department"],
                "job_family": match["job_family"],
                "role_key": match["role_key"],
                "occupation_key": match["role_key"],
                "seniority_level": match["seniority_level"],
                "job_role_type": match["job_role_type"],

                "country": safe_value(row, "country"),
                "location": safe_value(row, "location") if "location" in arabjobs.columns else "unknown",
                "original_gender_label": safe_value(row, "gender"),
                "job_category": safe_value(row, "job_category"),
                "sub_category": safe_value(row, "sub_category"),
                "profession": safe_value(row, "profession"),
                "original_job_title": safe_value(row, "job_title"),

                "matched_form": match["matched_form"],
                "stereotype_label": "not_applicable",

                "masculine_occupation": match["masculine_job_title"],
                "feminine_occupation": match["feminine_job_title"],
                "masculine_job_title": match["masculine_job_title"],
                "feminine_job_title": match["feminine_job_title"],

                "template_id": template["template_id"],
                "template_type": template["template_type"],
                "semantic_frame": template["semantic_frame"],
                "dialect": template["dialect"],

                "masculine_sentence": masculine_sentence,
                "feminine_sentence": feminine_sentence,

                "source_type": "external_real_world_job_ad_corpus",
                "needs_human_validation": True,
            })

            pair_index += 1

    matched_df = pd.DataFrame(matched_rows)
    unmatched_df = pd.DataFrame(unmatched_rows)
    pairs_df = pd.DataFrame(pair_rows)

    matched_df.to_csv(MATCHED_ROWS, index=False, encoding="utf-8-sig")
    unmatched_df.head(500).to_csv(UNMATCHED_ROWS, index=False, encoding="utf-8-sig")
    pairs_df.to_csv(OUTPUT_PAIRS, index=False, encoding="utf-8-sig")

    summary_rows = [
        {"metric": "arabjobs_total_rows", "value": len(arabjobs)},
        {"metric": "matched_rows", "value": len(matched_df)},
        {"metric": "unmatched_rows", "value": len(unmatched_df)},
        {"metric": "counterfactual_pairs", "value": len(pairs_df)},
        {"metric": "templates_per_matched_row", "value": len(TEMPLATES)},
        {"metric": "unique_countries_matched", "value": matched_df["country"].nunique() if not matched_df.empty else 0},
        {"metric": "unique_job_categories_matched", "value": matched_df["job_category"].nunique() if not matched_df.empty else 0},
        {"metric": "unique_departments_matched", "value": matched_df["department"].nunique() if not matched_df.empty else 0},
        {"metric": "unique_roles_matched", "value": matched_df["role_key"].nunique() if not matched_df.empty else 0},
        {"metric": "requires_manual_validation", "value": True},
    ]

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    doc = []
    doc.append("# ArabJobs v7 External Dataset Integration Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "This integration adds ArabJobs as an external real-world Arabic job-ad corpus to the occupational gender-bias evaluation framework."
    )
    doc.append("")
    doc.append("## Source")
    doc.append("")
    doc.append("- Dataset: ArabJobs: A Multinational Corpus of Arabic Job Ads")
    doc.append("- Source file: data/external_datasets/arabjobs/ArabJobs.csv")
    doc.append("- Integrated output: data/external_datasets/arabjobs/arabjobs_v7_counterfactual_pairs.csv")
    doc.append("")
    doc.append("## Preparation Summary")
    doc.append("")
    for row in summary_rows:
        doc.append(f"- {row['metric']}: {row['value']}")
    doc.append("")
    doc.append("## Method")
    doc.append("")
    doc.append(
        "The converter matches ArabJobs job titles, professions, and descriptions against the v6 masculine-feminine job-role lexicon. "
        "Matched rows are converted into controlled masculine-feminine counterfactual sentence pairs while preserving ArabJobs metadata "
        "such as country, original gender label, job category, sub-category, profession, and original job title."
    )
    doc.append("")
    doc.append("## Thesis Value")
    doc.append("")
    doc.append(
        "ArabJobs strengthens the thesis by adding external validation from real Arabic recruitment texts across multiple Arab countries. "
        "It supports a stronger claim that the proposed framework can move from controlled benchmark construction to real-world job-ad contexts."
    )
    doc.append("")
    doc.append("## Important Limitation")
    doc.append("")
    doc.append(
        "The generated pairs require human validation because real-world job advertisements may contain noisy titles, mixed dialects, inconsistent gender markers, or multi-role descriptions."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("ArabJobs v7 preparation completed.")
    print("Pairs:", OUTPUT_PAIRS)
    print("Matched rows:", MATCHED_ROWS)
    print("Unmatched sample:", UNMATCHED_ROWS)
    print("Summary:", SUMMARY_PATH)
    print("Doc:", DOC_PATH)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()