from pathlib import Path
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

RAW_TEXT_PATH = OUTPUT_DIR / "scraped_raw_text_debug.txt"
CONTEXTS_CSV = OUTPUT_DIR / "scraped_contexts_debug.csv"
MENTIONS_CSV = OUTPUT_DIR / "scraped_job_title_mentions.csv"
PAIRS_CSV = DATA_OUTPUT_DIR / "scraped_job_title_bias_pairs.csv"
SUMMARY_CSV = OUTPUT_DIR / "scraped_job_title_measurement_summary.csv"
SUMMARY_MD = Path("docs/occupational_scope/scraped_job_title_measurement_summary.md")

USER_AGENT = "ArabicBiasResearchBot/1.0 academic-research"
REQUEST_TIMEOUT = 30
SLEEP_SECONDS = 1


PAIR_COLUMNS = [
    "id",
    "benchmark_version",
    "occupation_id",
    "field",
    "occupation_key",
    "occupation_en",
    "masculine_occupation",
    "feminine_occupation",
    "stereotype_label",
    "dialect",
    "template_id",
    "template_type",
    "semantic_frame",
    "grammatical_gender_marker",
    "source_id",
    "source_name",
    "source_type",
    "source_url",
    "original_context_text",
    "original_matched_gender",
    "matched_form",
    "match_source",
    "masculine_sentence",
    "feminine_sentence",
    "needs_manual_review",
    "review_reason",
]


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
    html = unescape(str(html))

    html = re.sub(r"(?is)<script.*?>.*?</script>", "\n", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", "\n", html)

    # Preserve important HTML boundaries.
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(
        r"(?i)</(p|div|li|ul|ol|h1|h2|h3|h4|h5|h6|a|section|article|span)>",
        "\n",
        html,
    )
    html = re.sub(
        r"(?i)<(p|div|li|ul|ol|h1|h2|h3|h4|h5|h6|a|section|article|span)[^>]*>",
        "\n",
        html,
    )

    html = re.sub(r"(?is)<[^>]+>", " ", html)

    lines = []
    for line in html.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()
        if cleaned:
            lines.append(cleaned)

    return "\n".join(lines)


def split_contexts(text):
    contexts = []

    for line in str(text).splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()

        if 3 <= len(cleaned) <= 250:
            contexts.append(cleaned)

        if len(cleaned) > 250:
            parts = re.split(r"[.!؟?؛،]+", cleaned)
            for part in parts:
                part = re.sub(r"\s+", " ", part).strip()
                if 3 <= len(part) <= 250:
                    contexts.append(part)

    # Also extract common job-title phrases from the full text.
    full_text = re.sub(r"\s+", " ", str(text))
    title_patterns = [
        r"مطلوب\s+[^.!؟?؛،\n\r]{2,80}",
        r"وظائف\s+[^.!؟?؛،\n\r]{2,80}",
    ]

    for pattern in title_patterns:
        for match in re.findall(pattern, full_text):
            cleaned = re.sub(r"\s+", " ", match).strip()
            if 3 <= len(cleaned) <= 250:
                contexts.append(cleaned)

    seen = set()
    unique_contexts = []

    for context in contexts:
        if context not in seen:
            seen.add(context)
            unique_contexts.append(context)

    return unique_contexts


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

    return raw.decode(encoding, errors="replace")


def add_lookup_item(
    lookup,
    occupation_id,
    field,
    occupation_key,
    occupation_en,
    stereotype_label,
    masculine_occupation,
    feminine_occupation,
    matched_gender,
    matched_form,
    match_source,
):
    lookup.append({
        "occupation_id": occupation_id,
        "field": field,
        "occupation_key": occupation_key,
        "occupation_en": occupation_en,
        "stereotype_label": stereotype_label,
        "masculine_occupation": masculine_occupation,
        "feminine_occupation": feminine_occupation,
        "matched_gender": matched_gender,
        "matched_form": matched_form,
        "match_source": match_source,
    })


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

            add_lookup_item(
                lookup=lookup,
                occupation_id=row["occupation_id"],
                field=row.get("field", ""),
                occupation_key=row.get("occupation_key", ""),
                occupation_en=row.get("occupation_en", ""),
                stereotype_label=row.get("stereotype_label", ""),
                masculine_occupation=row["masculine_occupation"],
                feminine_occupation=row["feminine_occupation"],
                matched_gender=gender_label,
                matched_form=form,
                match_source="lexicon_exact",
            )

    # Common public job-board aliases.
    aliases = [
        ("driver", "عمال وخدمات", "سائق", "سائقة", ["سائق", "سائق خاص", "سائقين"]),
        ("civil_engineer", "هندسة", "مهندس مدني", "مهندسة مدنية", ["مهندس مدني", "مهندسين مدني"]),
        ("mechanical_engineer", "هندسة", "مهندس ميكانيكا", "مهندسة ميكانيكا", ["مهندس ميكانيكا", "مهندسين ميكانيكا"]),
        ("electrical_engineer", "هندسة", "مهندس كهرباء", "مهندسة كهرباء", ["مهندس كهرباء", "مهندسين كهرباء"]),
        ("architect", "هندسة", "مهندس معماري", "مهندسة معمارية", ["مهندس معماري", "مهندسين معماري"]),
        ("sales_engineer", "بيع وتسويق", "مهندس مبيعات", "مهندسة مبيعات", ["مهندس مبيعات"]),
        ("agricultural_engineer", "علمية وزراعية", "مهندس زراعي", "مهندسة زراعية", ["مهندس زراعي", "مهندسين زراعيين"]),
        ("accountant", "مال ومحاسبة", "محاسب", "محاسبة", ["محاسب", "محاسبين"]),
        ("auditor", "مال ومحاسبة", "مدقق حسابات", "مدققة حسابات", ["مدقق حسابات"]),
        ("account_manager", "مال ومحاسبة", "مدير حسابات", "مديرة حسابات", ["مدير حسابات"]),
        ("lawyer", "قانون", "محامي", "محامية", ["محامي", "محامين"]),
        ("secretary", "ادارة", "سكرتير", "سكرتيرة", ["سكرتير", "سكرتيرة", "سكرتارية"]),
        ("call_center", "خدمة عملاء", "موظف كول سنتر", "موظفة كول سنتر", ["كول سنتر", "موظف كول سنتر"]),
        ("security_guard", "امن", "فرد أمن", "فردة أمن", ["فرد أمن", "أفراد أمن", "افراد أمن", "موظف امن"]),
        ("data_entry", "ادارة", "مدخل بيانات", "مدخلة بيانات", ["مدخل بيانات", "مدخلين بيانات"]),
        ("pharmacist", "طب وصحة", "صيدلي", "صيدلانية", ["صيدلي", "صيادلة"]),
        ("graphic_designer", "تصميم وفنون", "مصمم جرافيك", "مصممة جرافيك", ["مصمم جرافيك"]),
        ("sales_representative", "بيع وتسويق", "مندوب مبيعات", "مندوبة مبيعات", ["مندوب مبيعات", "مندوب"]),
        ("purchasing_representative", "ادارة", "مندوب مشتريات", "مندوبة مشتريات", ["مندوب مشتريات"]),
        ("dentist_assistant", "طب وصحة", "مساعد طبيب أسنان", "مساعدة طبيب أسنان", ["مساعدة طبيب أسنان", "مساعد طبيب أسنان"]),
        ("seller", "بيع وتسويق", "بائع", "بائعة", ["بائع", "بائعين"]),
        ("surveyor", "هندسة", "مساح", "مساحة", ["مساح", "مساحين"]),
    ]

    for occupation_key, field, masculine_form, feminine_form, forms in aliases:
        for form in forms:
            matched_gender = "feminine" if form in [feminine_form] else "masculine"

            add_lookup_item(
                lookup=lookup,
                occupation_id=f"scraped_alias_{occupation_key}",
                field=field,
                occupation_key=occupation_key,
                occupation_en=occupation_key,
                stereotype_label="unknown_scraped_alias",
                masculine_occupation=masculine_form,
                feminine_occupation=feminine_form,
                matched_gender=matched_gender,
                matched_form=form,
                match_source="fallback_alias",
            )

    lookup = sorted(lookup, key=lambda x: len(x["matched_form"]), reverse=True)
    return lookup


def find_mentions(context, occupation_lookup):
    mentions = []

    for item in occupation_lookup:
        form = item["matched_form"]

        if form and form in context:
            mentions.append(item)

    return mentions


def build_counterfactual_pair(context, mention):
    masculine_form = str(mention["masculine_occupation"]).strip()
    feminine_form = str(mention["feminine_occupation"]).strip()
    matched_form = str(mention["matched_form"]).strip()

    if mention["matched_gender"] == "feminine":
        feminine_sentence = context
        masculine_sentence = context.replace(matched_form, masculine_form, 1)
        original_gender = "feminine"
    else:
        masculine_sentence = context
        feminine_sentence = context.replace(matched_form, feminine_form, 1)
        original_gender = "masculine"

    return masculine_sentence, feminine_sentence, original_gender


def write_empty_outputs(status, enabled_sources_count=0):
    pd.DataFrame().to_csv(MENTIONS_CSV, index=False, encoding="utf-8-sig")
    pd.DataFrame(columns=PAIR_COLUMNS).to_csv(PAIRS_CSV, index=False, encoding="utf-8-sig")

    summary_df = pd.DataFrame([
        {"metric": "enabled_sources", "value": enabled_sources_count},
        {"metric": "scraped_mentions", "value": 0},
        {"metric": "counterfactual_pairs", "value": 0},
        {"metric": "unique_occupations", "value": 0},
        {"metric": "unique_fields", "value": 0},
        {"metric": "manual_review_required", "value": True},
        {"metric": "status", "value": status},
    ])

    summary_df.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

    SUMMARY_MD.write_text(
        "# Scraped Job-Title Measurement Summary\n\n"
        f"Status: `{status}`\n\n"
        "This component is an external enrichment pilot.\n",
        encoding="utf-8",
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_MD.parent.mkdir(parents=True, exist_ok=True)

    if not LEXICON_PATH.exists():
        raise FileNotFoundError(f"Lexicon not found: {LEXICON_PATH}")

    if not SOURCES_PATH.exists():
        raise FileNotFoundError(f"Sources file not found: {SOURCES_PATH}")

    lexicon_df = pd.read_csv(LEXICON_PATH, encoding="utf-8-sig")
    lexicon_df = normalize_lexicon_columns(lexicon_df)
    occupation_lookup = build_occupation_lookup(lexicon_df)

    sources_df = pd.read_csv(SOURCES_PATH, encoding="utf-8-sig")
    sources_df["enabled"] = (
        sources_df["enabled"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    enabled_sources = sources_df[sources_df["enabled"] == True].copy()

    if enabled_sources.empty:
        write_empty_outputs("no_enabled_sources", 0)
        print("No enabled sources found.")
        return

    all_raw_text = []
    context_rows = []
    mention_rows = []

    for _, source in enabled_sources.iterrows():
        source_id = source["source_id"]
        source_name = source["source_name"]
        source_type = source["source_type"]
        url = source["url"]

        print(f"Processing: {source_id} | {url}")

        if not robots_allowed(url):
            print(f"Skipped by robots.txt: {url}")
            continue

        try:
            html = fetch_url(url)
            text = html_to_text(html)
            contexts = split_contexts(text)

            all_raw_text.append(f"\n\n===== SOURCE: {source_id} | {url} =====\n\n{text}")

            for context_idx, context in enumerate(contexts):
                context_rows.append({
                    "source_id": source_id,
                    "source_url": url,
                    "context_index": context_idx,
                    "context_text": context,
                })

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

    RAW_TEXT_PATH.write_text("\n".join(all_raw_text), encoding="utf-8")
    pd.DataFrame(context_rows).to_csv(CONTEXTS_CSV, index=False, encoding="utf-8-sig")

    mentions_df = pd.DataFrame(mention_rows)

    if mentions_df.empty:
        write_empty_outputs("no_occupation_mentions_found", len(enabled_sources))
        print("No occupation mentions found.")
        print("Check debug file:", RAW_TEXT_PATH)
        print("Check contexts:", CONTEXTS_CSV)
        return

    mentions_df = mentions_df.drop_duplicates(
        subset=[
            "source_url",
            "context_text",
            "occupation_id",
            "matched_gender",
            "matched_form",
        ]
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

    pairs_df = pd.DataFrame(pair_rows, columns=PAIR_COLUMNS)

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
        {"metric": "status", "value": "completed"},
    ])

    summary_df.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Scraped Job-Title Measurement Summary")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This pilot collects public Arabic job-title mentions, matches them to an occupation lexicon, "
        "and builds masculine-feminine counterfactual pairs."
    )
    md.append("")
    md.append("## Summary")
    md.append("")
    for _, row in summary_df.iterrows():
        md.append(f"- {row['metric']}: {row['value']}")
    md.append("")
    md.append("## Output Files")
    md.append("")
    md.append(f"- Raw text debug: `{RAW_TEXT_PATH}`")
    md.append(f"- Contexts debug: `{CONTEXTS_CSV}`")
    md.append(f"- Mentions: `{MENTIONS_CSV}`")
    md.append(f"- Pairs: `{PAIRS_CSV}`")
    md.append(f"- Summary: `{SUMMARY_CSV}`")
    md.append("")
    md.append("## Note")
    md.append("")
    md.append(
        "This remains an external enrichment pilot because scraped counterfactual replacements "
        "may require manual grammatical review."
    )
    md.append("")

    SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")

    print("Scraping and measurement pair construction completed.")
    print("Summary:", SUMMARY_CSV)
    print("Pairs:", PAIRS_CSV)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
