from pathlib import Path
import pandas as pd
import numpy as np


OUTPUT_DIR = Path("results/final_package")
OUTPUT_CSV = OUTPUT_DIR / "bootstrap_bias_score_confidence_intervals.csv"
OUTPUT_MD = Path("docs/occupational_scope/bootstrap_confidence_intervals_summary.md")


SEARCH_DIRS = [
    Path("results/occupational_benchmark_v2_all_models"),
    Path("results/occupational_benchmark_v3_balanced_quick_models"),
    Path("results/occupational_benchmark_v4_template_perturbation_all_models"),
    Path("results/occupational_benchmark_v5_job_titles_quick_models"),
]


REQUIRED_COLUMNS = [
    "model_name",
    "score_difference",
]


N_BOOTSTRAP = 5000
CONFIDENCE_LEVEL = 0.95
RANDOM_SEED = 42


def infer_benchmark_from_path(path):
    text = str(path).lower()

    if "v5" in text:
        return "v5"
    if "v4" in text:
        return "v4"
    if "v3_balanced" in text:
        return "v3_balanced"
    if "v2" in text:
        return "v2"

    return "unknown"


def is_candidate_file(path):
    if path.suffix.lower() != ".csv":
        return False

    name = path.name.lower()

    excluded_terms = [
        "summary",
        "counts",
        "quality",
        "chi_square",
        "cramers",
        "effect",
        "volatility",
        "dialect_shift",
        "registry",
        "matrix",
        "taxonomy",
        "confidence_intervals",
    ]

    if any(term in name for term in excluded_terms):
        return False

    return True


def read_scored_file(path):
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return None

    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        return None

    df = df.copy()
    df["score_difference"] = pd.to_numeric(df["score_difference"], errors="coerce")
    df = df.dropna(subset=["score_difference"])

    if df.empty:
        return None

    df["benchmark"] = infer_benchmark_from_path(path)
    df["source_file"] = str(path)

    if "id" not in df.columns:
        df["id"] = ""

    return df


def collect_scored_rows():
    frames = []

    for directory in SEARCH_DIRS:
        if not directory.exists():
            print(f"Skipping missing directory: {directory}")
            continue

        for path in directory.rglob("*.csv"):
            if not is_candidate_file(path):
                continue

            df = read_scored_file(path)
            if df is not None:
                frames.append(df)

    if not frames:
        raise ValueError("No scored result rows found.")

    combined = pd.concat(frames, ignore_index=True)

    combined = combined.drop_duplicates(
        subset=[
            "benchmark",
            "model_name",
            "id",
            "score_difference",
        ],
        keep="first",
    )

    return combined


def direction_from_value(value):
    if value > 0:
        return "masculine"
    if value < 0:
        return "feminine"
    return "equal"


def bootstrap_mean_ci(values, n_bootstrap=N_BOOTSTRAP, confidence_level=CONFIDENCE_LEVEL):
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(RANDOM_SEED)

    if len(values) == 0:
        return None

    bootstrap_means = []

    for _ in range(n_bootstrap):
        sample = rng.choice(values, size=len(values), replace=True)
        bootstrap_means.append(sample.mean())

    bootstrap_means = np.asarray(bootstrap_means)

    alpha = 1 - confidence_level
    lower = np.quantile(bootstrap_means, alpha / 2)
    upper = np.quantile(bootstrap_means, 1 - alpha / 2)

    return float(lower), float(upper)


def classify_ci_direction(lower, upper):
    if lower > 0 and upper > 0:
        return "reliably_masculine"
    if lower < 0 and upper < 0:
        return "reliably_feminine"
    return "uncertain_crosses_zero"


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
                value = f"{value:.5f}"
            values.append(str(value).replace("|", "/"))
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    scored_df = collect_scored_rows()

    rows = []

    for (benchmark, model_name), group in scored_df.groupby(["benchmark", "model_name"]):
        values = group["score_difference"].values

        ci_lower, ci_upper = bootstrap_mean_ci(values)

        mean_value = float(np.mean(values))
        median_value = float(np.median(values))
        std_value = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0

        rows.append({
            "benchmark": benchmark,
            "model_name": model_name,
            "n_items": len(values),
            "mean_score_difference": mean_value,
            "median_score_difference": median_value,
            "std_score_difference": std_value,
            "ci_level": CONFIDENCE_LEVEL,
            "bootstrap_iterations": N_BOOTSTRAP,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "mean_direction": direction_from_value(mean_value),
            "ci_direction_classification": classify_ci_direction(ci_lower, ci_upper),
        })

    result_df = pd.DataFrame(rows)
    result_df = result_df.sort_values(["benchmark", "model_name"])

    result_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    md = []
    md.append("# Bootstrap Confidence Intervals for Bias Scores")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(
        "This analysis estimates uncertainty around the average score difference "
        "for each model and benchmark."
    )
    md.append("")
    md.append("The score is defined as:")
    md.append("")
    md.append("```text")
    md.append("score_difference = masculine_score - feminine_score")
    md.append("```")
    md.append("")
    md.append("A positive mean indicates masculine preference. A negative mean indicates feminine preference.")
    md.append("")
    md.append("## Method")
    md.append("")
    md.append(
        f"For each model and benchmark, the analysis uses {N_BOOTSTRAP} bootstrap resamples "
        f"to estimate a {int(CONFIDENCE_LEVEL * 100)}% confidence interval for the mean score difference."
    )
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("- If the confidence interval is entirely above zero, the result is classified as reliably masculine.")
    md.append("- If the confidence interval is entirely below zero, the result is classified as reliably feminine.")
    md.append("- If the confidence interval crosses zero, the result is classified as uncertain or near-neutral.")
    md.append("")
    md.append("## Results")
    md.append("")
    md.append(markdown_table(result_df))
    md.append("")
    md.append("## Contribution")
    md.append("")
    md.append(
        "This analysis enriches the thesis by adding uncertainty estimation to the bias scores. "
        "It helps distinguish strong directional findings from weak or near-neutral effects."
    )
    md.append("")
    md.append(
        "This is especially useful for benchmarks such as v5, where average score differences "
        "can be small and close to zero."
    )
    md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("Bootstrap confidence interval analysis completed.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)
    print("")
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    main()