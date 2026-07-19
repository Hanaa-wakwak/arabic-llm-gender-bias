from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/final_package")
OUTPUT_DETAILED_CSV = OUTPUT_DIR / "counterfactual_pair_integrity_detailed.csv"
OUTPUT_SUMMARY_CSV = OUTPUT_DIR / "counterfactual_pair_integrity_summary.csv"
OUTPUT_MD = Path("docs/occupational_scope/counterfactual_pair_integrity_audit.md")


BENCHMARK_FILES = [
    {
        "benchmark": "v2",
        "path": Path("data/occupational_benchmark/occupational_bias_v2.csv"),
    },
    {
        "benchmark": "v3",
        "path": Path("data/occupational_benchmark/occupational_bias_v3.csv"),
    },
    {
        "benchmark": "v3_controlled",
        "path": Path("data/occupational_benchmark/occupational_bias_v3_controlled.csv"),
    },
    {
        "benchmark": "v3_balanced",
        "path": Path("data/occupational_benchmark/occupational_bias_v3_balanced.csv"),
    },
    {
        "benchmark": "v4",
        "path": Path("data/occupational_benchmark/occupational_bias_v4_template_perturbation.csv"),
    },
    {
        "benchmark": "v5",
        "path": Path("data/occupational_benchmark/occupational_bias_v5_job_titles.csv"),
    },
]


REQUIRED_COLUMNS = [
    "masculine_sentence",
    "feminine_sentence",
]


def read_optional(path):
    if not path.exists():
        print(f"Skipping missing benchmark: {path}")
        return None

    return pd.read_csv(path, encoding="utf-8-sig")


def simple_word_count(text):
    return len(str(text).split())


def normalize_text(text):
    return str(text).strip()


def get_optional_value(row, column):
    if column in row.index:
        return row[column]
    return ""


def audit_file(benchmark_name, path):
    df = read_optional(path)

    if df is None:
        return pd.DataFrame()

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"{path} missing required columns: {missing}")

    rows = []

    for idx, row in df.iterrows():
        masculine_sentence = normalize_text(row["masculine_sentence"])
        feminine_sentence = normalize_text(row["feminine_sentence"])

        masculine_chars = len(masculine_sentence)
        feminine_chars = len(feminine_sentence)

        masculine_words = simple_word_count(masculine_sentence)
        feminine_words = simple_word_count(feminine_sentence)

        char_diff = masculine_chars - feminine_chars
        word_diff = masculine_words - feminine_words

        masculine_occupation = str(get_optional_value(row, "masculine_occupation"))
        feminine_occupation = str(get_optional_value(row, "feminine_occupation"))

        masculine_occupation_present = (
            masculine_occupation.strip() != ""
            and masculine_occupation.strip() in masculine_sentence
        )

        feminine_occupation_present = (
            feminine_occupation.strip() != ""
            and feminine_occupation.strip() in feminine_sentence
        )

        rows.append({
            "benchmark": benchmark_name,
            "source_file": str(path),
            "row_index": idx,
            "id": get_optional_value(row, "id"),
            "field": get_optional_value(row, "field"),
            "dialect": get_optional_value(row, "dialect"),
            "template_id": get_optional_value(row, "template_id"),
            "semantic_frame": get_optional_value(row, "semantic_frame"),
            "stereotype_label": get_optional_value(row, "stereotype_label"),
            "masculine_sentence": masculine_sentence,
            "feminine_sentence": feminine_sentence,
            "masculine_chars": masculine_chars,
            "feminine_chars": feminine_chars,
            "char_diff_m_minus_f": char_diff,
            "abs_char_diff": abs(char_diff),
            "masculine_words": masculine_words,
            "feminine_words": feminine_words,
            "word_diff_m_minus_f": word_diff,
            "abs_word_diff": abs(word_diff),
            "sentences_identical": masculine_sentence == feminine_sentence,
            "masculine_occupation": masculine_occupation,
            "feminine_occupation": feminine_occupation,
            "masculine_occupation_present": masculine_occupation_present,
            "feminine_occupation_present": feminine_occupation_present,
        })

    return pd.DataFrame(rows)


def summarize(detailed_df):
    summary_rows = []

    for benchmark, group in detailed_df.groupby("benchmark"):
        summary_rows.append({
            "benchmark": benchmark,
            "total_pairs": len(group),
            "identical_sentence_pairs": int(group["sentences_identical"].sum()),
            "average_abs_char_diff": group["abs_char_diff"].mean(),
            "median_abs_char_diff": group["abs_char_diff"].median(),
            "max_abs_char_diff": group["abs_char_diff"].max(),
            "average_abs_word_diff": group["abs_word_diff"].mean(),
            "median_abs_word_diff": group["abs_word_diff"].median(),
            "max_abs_word_diff": group["abs_word_diff"].max(),
            "masculine_occupation_missing_count": int((group["masculine_occupation_present"] == False).sum()),
            "feminine_occupation_missing_count": int((group["feminine_occupation_present"] == False).sum()),
        })

    return pd.DataFrame(summary_rows)


def markdown_table(df):
    cols = list(df.columns)
    lines = []

    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                value = f"{value:.4f}"
            values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    frames = []

    for item in BENCHMARK_FILES:
        audited = audit_file(item["benchmark"], item["path"])
        if not audited.empty:
            frames.append(audited)

    if not frames:
        raise ValueError("No benchmark files were audited.")

    detailed_df = pd.concat(frames, ignore_index=True)
    summary_df = summarize(detailed_df)

    detailed_df.to_csv(OUTPUT_DETAILED_CSV, index=False, encoding="utf-8-sig")
    summary_df.to_csv(OUTPUT_SUMMARY_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Counterfactual Pair Integrity Audit")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This audit checks whether masculine and feminine sentence pairs are structurally comparable "
        "across the benchmark suite."
    )
    md.append("")
    md.append(
        "The goal is to support the counterfactual design by verifying that sentence pairs differ mainly "
        "in the gendered occupational form rather than uncontrolled sentence structure."
    )
    md.append("")
    md.append("## What the Audit Checks")
    md.append("")
    md.append("- masculine and feminine sentence length,")
    md.append("- absolute character-length difference,")
    md.append("- absolute word-count difference,")
    md.append("- identical sentence errors,")
    md.append("- whether the masculine occupation appears in the masculine sentence,")
    md.append("- whether the feminine occupation appears in the feminine sentence.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(markdown_table(summary_df))
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append(
        "Low average word-count differences indicate that the masculine and feminine sentence variants "
        "are structurally close. This strengthens the validity of the likelihood comparison because the "
        "model is comparing near-counterfactual sentence pairs."
    )
    md.append("")
    md.append(
        "This audit does not prove perfect semantic equivalence, but it provides an implementation-level "
        "quality-control layer for the benchmark design."
    )
    md.append("")
    md.append("## Contribution")
    md.append("")
    md.append(
        "This audit adds a methodological validation layer to the thesis. It shows that the benchmark suite "
        "does not only generate sentence pairs, but also checks the integrity of the counterfactual pair design."
    )
    md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("Counterfactual pair integrity audit created.")
    print("Detailed CSV:", OUTPUT_DETAILED_CSV)
    print("Summary CSV:", OUTPUT_SUMMARY_CSV)
    print("Markdown:", OUTPUT_MD)
    print("")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()