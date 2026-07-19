from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/final_package")
OUTPUT_CSV = OUTPUT_DIR / "benchmark_design_taxonomy.csv"
OUTPUT_MD = Path("docs/occupational_scope/benchmark_design_taxonomy.md")


ROWS = [
    {
        "benchmark": "v2",
        "role": "main_validated_benchmark",
        "occupation_count": 60,
        "template_count": 4,
        "sentence_pair_count": 240,
        "dialects": "MSA, Egyptian",
        "semantic_frames": "workplace_presence, professional_statement",
        "stereotype_balance": "not_fully_balanced",
        "main_context": "general occupational workplace sentences",
        "main_question": "Do models prefer masculine or feminine occupational sentence variants?",
        "technical_value": "core validated benchmark and six-model model-family comparison",
    },
    {
        "benchmark": "v3",
        "role": "expansion_sensitivity",
        "occupation_count": 90,
        "template_count": 6,
        "sentence_pair_count": 540,
        "dialects": "MSA, Egyptian",
        "semantic_frames": "expanded occupational sentence frames",
        "stereotype_balance": "partially controlled",
        "main_context": "expanded occupation and template coverage",
        "main_question": "Does expanding the benchmark change measured bias direction?",
        "technical_value": "tests sensitivity to occupation coverage and template expansion",
    },
    {
        "benchmark": "v3_controlled",
        "role": "occupation_vs_template_diagnostic",
        "occupation_count": 90,
        "template_count": 4,
        "sentence_pair_count": 360,
        "dialects": "MSA, Egyptian",
        "semantic_frames": "original v2-style frames",
        "stereotype_balance": "partially controlled",
        "main_context": "expanded occupations with original templates",
        "main_question": "Is the direction shift caused only by new templates?",
        "technical_value": "separates occupation-set effects from template-set effects",
    },
    {
        "benchmark": "v3_balanced",
        "role": "stereotype_balanced_sensitivity",
        "occupation_count": 90,
        "template_count": 4,
        "sentence_pair_count": 360,
        "dialects": "MSA, Egyptian",
        "semantic_frames": "original v2-style frames",
        "stereotype_balance": "30 male-stereotyped, 30 female-stereotyped, 30 neutral",
        "main_context": "balanced occupation stereotype labels",
        "main_question": "Does stereotype balancing stabilize measured bias direction?",
        "technical_value": "tests robustness after stereotype-label balancing",
    },
    {
        "benchmark": "v4",
        "role": "template_semantic_frame_dialect_sensitivity",
        "occupation_count": 90,
        "template_count": 8,
        "sentence_pair_count": 720,
        "dialects": "MSA, Egyptian",
        "semantic_frames": "occupation_presence, professional_experience, leadership, competence, achievement_reward, responsibility_trust",
        "stereotype_balance": "30 male-stereotyped, 30 female-stereotyped, 30 neutral",
        "main_context": "template perturbation and semantic-frame variation",
        "main_question": "Does measured bias flip across templates, semantic frames, and dialects?",
        "technical_value": "introduces template-induced direction volatility and effect-size analysis",
    },
    {
        "benchmark": "v5",
        "role": "explicit_job_title_context_sensitivity",
        "occupation_count": 90,
        "template_count": 6,
        "sentence_pair_count": 540,
        "dialects": "MSA, Egyptian",
        "semantic_frames": "CV profile, job advertisement, HR record, professional profile",
        "stereotype_balance": "30 male-stereotyped, 30 female-stereotyped, 30 neutral",
        "main_context": "explicit professional job-title contexts",
        "main_question": "Do models prefer masculine or feminine job-title forms when occupations appear as direct titles?",
        "technical_value": "separates job-title preference from broader sentence-context preference",
    },
]


def markdown_table(df):
    cols = list(df.columns)
    lines = []

    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = str(row[col]).replace("\n", " ")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(ROWS)

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Benchmark Design Taxonomy")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This taxonomy summarizes how each benchmark version contributes a different "
        "design dimension to the Arabic occupational gender-bias evaluation suite."
    )
    md.append("")
    md.append("## Taxonomy Table")
    md.append("")
    md.append(markdown_table(df))
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append(
        "The benchmark suite is intentionally multi-version. Each version tests a different "
        "source of measurement sensitivity: occupation coverage, template design, stereotype "
        "balance, semantic frame, dialect, and job-title context."
    )
    md.append("")
    md.append("## Contribution")
    md.append("")
    md.append(
        "This taxonomy widens the contribution by presenting the thesis as a benchmark-design "
        "framework rather than a single Arabic bias dataset."
    )
    md.append("")
    md.append(
        "The thesis therefore contributes both empirical results and a methodology for testing "
        "whether Arabic occupational gender-bias measurements are robust to benchmark-design choices."
    )
    md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("Benchmark design taxonomy created.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)
    print("")
    print(df[["benchmark", "role", "technical_value"]].to_string(index=False))


if __name__ == "__main__":
    main()
