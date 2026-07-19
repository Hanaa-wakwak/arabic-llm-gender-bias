from pathlib import Path
import csv
import re
import time
import urllib.request
import urllib.parse
import urllib.robotparser
from html import unescape

import pandas as pd


LEXICON_PATH = Path("data/occupational_benchmark/occupations_fields_v3_balanced.csv")
SOURCES_PATH = Path("data/external_datasets/job_scraping/job_sources.csv")

OUTPUT_DIR = Path("results/external_datasets/job_scraping")
DATA_OUTPUT_DIR = Path("data/external_datasets/job_scraping")

MENTIONS_CSV = OUTPUT_DIR / "scraped_job_title_mentions.csv"
PAIRS_CSV = DATA_OUTPUT_DIR / "scraped_job_title_bias_pairs.csv"
SUMMARY_CSV = OUTPUT_DIR / "scraped_job_title_measurement_summary.csv"
SUMMARY_MD = Path("docs/occupational_scope/scraped_job_title_measurement_summary.md")

USER_AGENT = "ArabicBiasResearchBot/1.0 academic-research-contact"
REQUEST_TIMEOUT = 20
SLEEP_SECONDS = 2


def normalize_lexicon_columns(df):
    df = df.copy()

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

    if "occupation_id" not in df.columns:
        if "occupation_key" in df.columns:
            df["occupation_id"] = [
                f"occ_{i + 1:03d}_{str(key).strip()}"
                for i, key in enumerate(df["occupation_key"])
            ]
        else:
            df["occupation_id"] = [f"occ_{i + 1:03d}" for i in range(len(df))]

    return df


def html_to_text(html):
    html = unescape(html)

    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)

    # Preserve meaningful HTML boundaries as new lines.
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</(p|div|li|ul|ol|h1|h2|h3|h4|h5|h6|a|section|article)>", "\n", html)
    html = re.sub(r"(?i)<(p|div|li|ul|ol|h1|h2|h3|h4|h5|h6|a|section|article)[^>]*>", "\n", html)

    html = re.sub(r"(?is)<[^>]+>", " ", html)

    lines = []
    for line in html.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()
        if cleaned:
            lines.append(cleaned)

    return "\n".join(lines)


def split_contexts(text):
    contexts = []

    # First keep natural HTML-derived lines.
    for line in text.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()

        if 4 <= len(cleaned) <= 300:
            contexts.append(cleaned)

        # Also split long lines by Arabic/English punctuation.
        if len(cleaned) > 300:
            parts = re.split(r"[.!؟?؛،]+", cleaned)
            for part in parts:
                part = re.sub(r"\s+", " ", part).strip()
                if 4 <= len(part) <= 300:
                    contexts.append(part)

    # Remove duplicates while preserving order.
    seen = set()
    unique_contexts = []

    for context in contexts:
        if context not in seen:
            seen.add(context)
            unique_contexts.append(context)

    return unique_contexts


def split_contexts(text):
    parts = re.split(r"[.!؟?؛،\n\r]+", text)
    contexts = []

    for part in parts:
        cleaned = re.sub(r"\s+", " ", part).strip()
        if 10 <= len(cleaned) <= 300:
            contexts.append(cleaned)

    return contexts


def robots_allowed(url):
    parsed = urllib.parse.urlparse(url)

    if not parsed.scheme or not parsed.netloc:
        return False

    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = urllib.robotparser.RobotFileParser()

    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(USER_AGENT, url)
    except Exception:
        # If robots cannot be checked, be conservative but allow manual research pages.
        # The URL and status are still recorded.
        return True


def fetch_url(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )

    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "")

    encoding = "utf-8"
    match = re.search(r"charset=([\w-]+)", content_type)
    if match:
        encoding = match.group(1)

    try:
        return raw.decode(encoding, errors="replace")
    except Exception:
        return raw.decode("utf-8", errors="replace")


def build_occupation_lookup(lexicon_df):
    lookup = []

    for _, row in lexicon_df.iterrows():
        for gender_label, col in [
            ("masculine", "masculine_occupation"),
            ("feminine", "feminine_occupation"),
        ]:
            form = str(row[col]).strip()
            if not form:
                continue

            lookup.append({
                "occupation_id": row["occupation_id"],
                "field": row.get("field", ""),
                "occupation_key": row.get("occupation_key", ""),
                "occupation_en": row.get("occupation_en", ""),
                "stereotype_label": row.get("stereotype_label", ""),
                "masculine_occupation": row["masculine_occupation"],
                "feminine_occupation": row["feminine_occupation"],
                "matched_gender": gender_label,
                "matched_form": form,
                "match_source": "lexicon_exact",
            })

    # Fallback aliases for common public job-board titles.
    fallback_aliases = [
        ("engineer", "هندسة", "مهندس", "مهندسة", ["مهندس", "مهندسين"]),
        ("civil_engineer", "هندسة", "مهندس مدني", "مهندسة مدنية", ["مهندس مدني", "مهندسين مدني"]),
        ("mechanical_engineer", "هندسة", "مهندس ميكانيكا", "مهندسة ميكانيكا", ["مهندس ميكانيكا", "مهندسين ميكانيكا"]),
        ("electrical_engineer", "هندسة", "مهندس كهرباء", "مهندسة كهرباء", ["مهندس كهرباء", "مهندسين كهرباء"]),
        ("architect", "هندسة", "مهندس معماري", "مهندسة معمارية", ["مهندس معماري", "مهندسين معماري"]),
        ("accountant", "مال ومحاسبة", "محاسب", "محاسبة", ["محاسب", "محاسبين"]),
        ("lawyer", "قانون", "محامي", "محامية", ["محامي", "محامين"]),
        ("secretary", "ادارة", "سكرتير", "سكرتيرة", ["سكرتير", "سكرتيرة", "سكرتارية"]),
        ("pharmacist", "طب وصحة", "صيدلي", "صيدلانية", ["صيدلي", "صيادلة"]),
        ("doctor", "طب وصحة", "طبيب", "طبيبة", ["طبيب", "اطباء", "أطباء"]),
        ("dentist", "طب وصحة", "طبيب أسنان", "طبيبة أسنان", ["طبيب أسنان", "طبيب اسنان", "اطباء اسنان", "أطباء أسنان"]),
        ("graphic_designer", "تصميم وفنون", "مصمم جرافيك", "مصممة جرافيك", ["مصمم جرافيك"]),
        ("sales_representative", "بيع وتسويق", "مندوب مبيعات", "مندوبة مبيعات", ["مندوب مبيعات", "مندوب"]),
        ("data_entry", "ادارة", "مدخل بيانات", "مدخلة بيانات", ["مدخل بيانات", "مدخلين بيانات"]),
        ("security_guard", "امن", "فرد أمن", "فردة أمن", ["فرد أمن", "افراد أمن", "أفراد أمن", "موظف امن"]),
        ("driver", "عمال وخدمات", "سائق", "سائقة", ["سائق", "سائقين"]),
    ]

    for occupation_key, field, masculine_form, feminine_form, aliases in fallback_aliases:
        for alias in aliases:
            lookup.append({
                "occupation_id": f"scraped_alias_{occupation_key}",
                "field": field,
                "occupation_key": occupation_key,
                "occupation_en": occupation_key,
                "stereotype_label": "unknown_scraped_alias",
                "masculine_occupation": masculine_form,
                "feminine_occupation": feminine_form,
                "matched_gender": "masculine",
                "matched_form": alias,
                "match_source": "fallback_alias",
            })

    # Match longer forms first to reduce partial overlap.
    lookup = sorted(lookup, key=lambda x: len(x["matched_form"]), reverse=True)
    return lookup

def find_mentions(context, occupation_lookup):
    mentions = []

    for item in occupation_lookup:
        form = item["matched_form"]

        if form in context:
            mentions.append(item)

    return mentions


def build_counterfactual_pair(context, mention):
    masculine_form = str(mention["masculine_occupation"]).strip()
    feminine_form = str(mention["feminine_occupation"]).strip()
    matched_form = str(mention["matched_form"]).strip()

    if mention["matched_gender"] == "masculine":
        masculine_sentence = context
        feminine_sentence = context.replace(matched_form, feminine_form, 1)
        original_gender = "masculine"
    else:
        feminine_sentence = context
        masculine_sentence = context.replace(matched_form, masculine_form, 1)
        original_gender = "feminine"

    return masculine_sentence, feminine_sentence, original_gender


def main():
    if not LEXICON_PATH.exists():
        raise FileNotFoundError(f"Lexicon not found: {LEXICON_PATH}")

    if not SOURCES_PATH.exists():
        raise FileNotFoundError(f"Sources file not found: {SOURCES_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_MD.parent.mkdir(parents=True, exist_ok=True)

    lexicon_df = pd.read_csv(LEXICON_PATH, encoding="utf-8-sig")
    lexicon_df = normalize_lexicon_columns(lexicon_df)

    occupation_lookup = build_occupation_lookup(lexicon_df)

    sources_df = pd.read_csv(SOURCES_PATH, encoding="utf-8-sig")
    sources_df["enabled"] = sources_df["enabled"].astype(str).str.lower().isin(["true", "1", "yes"])

    enabled_sources = sources_df[sources_df["enabled"] == True].copy()

    if enabled_sources.empty:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        SUMMARY_MD.parent.mkdir(parents=True, exist_ok=True)

        empty_mentions_df = pd.DataFrame()
        empty_pairs_df = pd.DataFrame()

        empty_mentions_df.to_csv(MENTIONS_CSV, index=False, encoding="utf-8-sig")
        empty_pairs_df.to_csv(PAIRS_CSV, index=False, encoding="utf-8-sig")

        summary_df = pd.DataFrame([
            {"metric": "enabled_sources", "value": 0},
            {"metric": "scraped_mentions", "value": 0},
            {"metric": "counterfactual_pairs", "value": 0},
            {"metric": "unique_occupations", "value": 0},
            {"metric": "unique_fields", "value": 0},
            {"metric": "manual_review_required", "value": True},
            {"metric": "status", "value": "no_enabled_sources"},
        ])

        summary_df.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

        md = []
        md.append("# Scraped Job-Title Measurement Summary")
        md.append("")
        md.append("No enabled scraping sources were found.")
        md.append("")
        md.append("Edit `data/external_datasets/job_scraping/job_sources.csv` and set `enabled=True` for at least one public Arabic job/career page.")
        md.append("")
        md.append("This component is an external enrichment pilot, not a replacement for the validated benchmark suite.")

        SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")

        print("No enabled sources found.")
        print("Empty pilot output files were created.")
        print("Summary:", SUMMARY_CSV)
        print("Pairs:", PAIRS_CSV)
        return

    mention_rows = []

    for _, source in enabled_sources.iterrows():
        source_id = source["source_id"]
        source_name = source["source_name"]
        source_type = source["source_type"]
        url = source["url"]

        print(f"Processing source: {source_id} | {url}")

        allowed = robots_allowed(url)

        if not allowed:
            print(f"Skipped by robots.txt: {url}")
            continue

        try:
            html = fetch_url(url)
            text = html_to_text(html)
            contexts = split_contexts(text)

            for context_idx, context in enumerate(contexts):
                mentions = find_mentions(context, occupation_lookup)

                for mention in mentions:
                    mention_rows.append({
                        "source_id": source_id,
                        "source_name": source_name,
                        "source_type": source_type,
                        "source_url": url,
                        "context_index": context_idx,
                        "context_text": context,
                        **mention,
                    })

            time.sleep(SLEEP_SECONDS)

        except Exception as e:
            print(f"Error fetching {url}: {e}")

    mentions_df = pd.DataFrame(mention_rows)

    if mentions_df.empty:
        empty_pairs_df = pd.DataFrame()
        empty_pairs_df.to_csv(PAIRS_CSV, index=False, encoding="utf-8-sig")

        summary_df = pd.DataFrame([
            {"metric": "enabled_sources", "value": len(enabled_sources)},
            {"metric": "scraped_mentions", "value": 0},
            {"metric": "counterfactual_pairs", "value": 0},
            {"metric": "unique_occupations", "value": 0},
            {"metric": "unique_fields", "value": 0},
            {"metric": "manual_review_required", "value": True},
            {"metric": "status", "value": "no_occupation_mentions_found"},
        ])

        summary_df.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

        md = []
        md.append("# Scraped Job-Title Measurement Summary")
        md.append("")
        md.append("The scraping run completed, but no matching occupation mentions were found.")
        md.append("")
        md.append("This may happen if the selected pages do not contain job titles from the benchmark lexicon.")
        md.append("")
        md.append("Try adding more Arabic job/career pages to `data/external_datasets/job_scraping/job_sources.csv`.")
        md.append("")
        md.append("This component remains an external enrichment pilot.")

        SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")

        print("No occupation mentions found.")
        print("Empty pilot pair file and summary were created.")
        print("Summary:", SUMMARY_CSV)
        print("Pairs:", PAIRS_CSV)
        return

    mentions_df = mentions_df.drop_duplicates(
        subset=["source_url", "context_text", "occupation_id", "matched_gender", "matched_form"]
    )

    mentions_df.to_csv(MENTIONS_CSV, index=False, encoding="utf-8-sig")

    pair_rows = []

    for idx, row in mentions_df.iterrows():
        masculine_sentence, feminine_sentence, original_gender = build_counterfactual_pair(
            row["context_text"],
            row,
        )

        pair_rows.append({
            "id": f"scraped_job_title__{idx + 1:05d}",
            "benchmark_version": "scraped_job_title_context_v1",
            "occupation_id": row["occupation_id"],
            "field": row["field"],
            "occupation_key": row["occupation_key"],
            "occupation_en": row["occupation_en"],
            "masculine_occupation": row["masculine_occupation"],
            "feminine_occupation": row["feminine_occupation"],
            "stereotype_label": row["stereotype_label"],
            "dialect": "unknown_scraped_arabic",
            "template_id": "scraped_job_title_context",
            "template_type": "scraped_context",
            "semantic_frame": "real_world_job_title_context",
            "grammatical_gender_marker": "scraped_gendered_occupation",
            "source_id": row["source_id"],
            "source_name": row["source_name"],
            "source_type": row["source_type"],
            "source_url": row["source_url"],
            "original_context_text": row["context_text"],
            "original_matched_gender": original_gender,
            "matched_form": row["matched_form"],
            "match_source": row.get("match_source", ""),
            "masculine_sentence": masculine_sentence,
            "feminine_sentence": feminine_sentence,
            "needs_manual_review": True,
            "review_reason": "scraped context counterfactual replacement may require agreement validation",
          
        })

    pairs_df = pd.DataFrame(pair_rows)

    pairs_df = pairs_df.drop_duplicates(
        subset=["masculine_sentence", "feminine_sentence", "occupation_id"]
    )

    pairs_df.to_csv(PAIRS_CSV, index=False, encoding="utf-8-sig")

    summary_df = pd.DataFrame([
        {"metric": "enabled_sources", "value": len(enabled_sources)},
        {"metric": "scraped_mentions", "value": len(mentions_df)},
        {"metric": "counterfactual_pairs", "value": len(pairs_df)},
        {"metric": "unique_occupations", "value": pairs_df["occupation_id"].nunique()},
        {"metric": "unique_fields", "value": pairs_df["field"].nunique()},
        {"metric": "manual_review_required", "value": True},
    ])

    summary_df.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Scraped Job-Title Measurement Summary")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This pipeline scrapes public Arabic web pages for occupational job-title mentions, "
        "matches them against the benchmark occupation lexicon, and builds masculine-feminine "
        "counterfactual sentence pairs for measurement."
    )
    md.append("")
    md.append("## Important Note")
    md.append("")
    md.append(
        "This is an external enrichment pilot, not a replacement for the validated manually "
        "constructed benchmarks. Scraped contexts may require manual review because replacing "
        "only the job title may not preserve full grammatical agreement."
    )
    md.append("")
    md.append("## Summary")
    md.append("")
    for _, row in summary_df.iterrows():
        md.append(f"- {row['metric']}: {row['value']}")
    md.append("")
    md.append("## Output Files")
    md.append("")
    md.append(f"- Mentions: `{MENTIONS_CSV}`")
    md.append(f"- Measurement pairs: `{PAIRS_CSV}`")
    md.append(f"- Summary: `{SUMMARY_CSV}`")
    md.append("")
    md.append("## Contribution")
    md.append("")
    md.append(
        "This adds a scraped real-world job-title context layer to the thesis. It helps test "
        "whether model behavior on manually constructed benchmarks is consistent with job-title "
        "mentions found in public Arabic text."
    )
    md.append("")

    SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")

    print("Scraping and measurement pair construction completed.")
    print("Mentions:", MENTIONS_CSV)
    print("Pairs:", PAIRS_CSV)
    print("Summary:", SUMMARY_CSV)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()