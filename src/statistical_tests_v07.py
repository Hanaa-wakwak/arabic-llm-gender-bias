from pathlib import Path
from itertools import combinations

import pandas as pd
from scipy.stats import binomtest, wilcoxon


INPUT_PATH = Path("results/model_comparison_v07/scoring_results_v07_all_models.csv")
OUTPUT_DIR = Path("results/statistical_tests_v07")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_binomial_test(group_df, group_info):
    masculine_count = int((group_df["preferred_gender"] == "masculine").sum())
    feminine_count = int((group_df["preferred_gender"] == "feminine").sum())
    total = masculine_count + feminine_count

    if total == 0:
        p_value = None
    else:
        p_value = binomtest(
            k=masculine_count,
            n=total,
            p=0.5,
            alternative="two-sided",
        ).pvalue

    masculine_percent = masculine_count / total * 100 if total else 0
    feminine_percent = feminine_count / total * 100 if total else 0

    if masculine_count > feminine_count:
        direction = "masculine"
    elif feminine_count > masculine_count:
        direction = "feminine"
    else:
        direction = "balanced"

    return {
        **group_info,
        "total_items": total,
        "masculine_preferred_count": masculine_count,
        "feminine_preferred_count": feminine_count,
        "masculine_preferred_percent": masculine_percent,
        "feminine_preferred_percent": feminine_percent,
        "preference_direction": direction,
        "binomial_p_value": p_value,
        "significant_at_0_05": p_value < 0.05 if p_value is not None else False,
    }


def run_wilcoxon_vs_zero(group_df, group_info):
    scores = group_df["score_difference"].dropna()

    if len(scores) == 0:
        statistic = None
        p_value = None
    else:
        try:
            result = wilcoxon(scores)
            statistic = result.statistic
            p_value = result.pvalue
        except ValueError:
            statistic = None
            p_value = None

    return {
        **group_info,
        "total_items": len(scores),
        "average_score_difference": scores.mean() if len(scores) else None,
        "median_score_difference": scores.median() if len(scores) else None,
        "wilcoxon_statistic": statistic,
        "wilcoxon_p_value": p_value,
        "significant_at_0_05": p_value < 0.05 if p_value is not None else False,
    }


def overall_tests(df):
    binomial_rows = []
    wilcoxon_rows = []

    for model_name, model_df in df.groupby("model_name"):
        group_info = {"model_name": model_name}

        binomial_rows.append(run_binomial_test(model_df, group_info))
        wilcoxon_rows.append(run_wilcoxon_vs_zero(model_df, group_info))

    binomial_df = pd.DataFrame(binomial_rows)
    wilcoxon_df = pd.DataFrame(wilcoxon_rows)

    binomial_df.to_csv(
        OUTPUT_DIR / "overall_binomial_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )

    wilcoxon_df.to_csv(
        OUTPUT_DIR / "overall_wilcoxon_vs_zero.csv",
        index=False,
        encoding="utf-8-sig",
    )


def grouped_binomial_tests(df, group_column):
    rows = []

    for group_values, group_df in df.groupby(["model_name", group_column]):
        model_name, group_value = group_values

        group_info = {
            "model_name": model_name,
            "group_type": group_column,
            "group_value": group_value,
        }

        rows.append(run_binomial_test(group_df, group_info))

    output_df = pd.DataFrame(rows)

    output_df.to_csv(
        OUTPUT_DIR / f"binomial_by_{group_column}.csv",
        index=False,
        encoding="utf-8-sig",
    )


def pairwise_model_wilcoxon(df):
    rows = []

    models = sorted(df["model_name"].unique())

    for model_a, model_b in combinations(models, 2):
        a = df[df["model_name"] == model_a][["id", "score_difference"]].copy()
        b = df[df["model_name"] == model_b][["id", "score_difference"]].copy()

        merged = a.merge(
            b,
            on="id",
            suffixes=("_a", "_b"),
        )

        diff = merged["score_difference_a"] - merged["score_difference_b"]

        try:
            result = wilcoxon(diff)
            statistic = result.statistic
            p_value = result.pvalue
        except ValueError:
            statistic = None
            p_value = None

        rows.append({
            "model_a": model_a,
            "model_b": model_b,
            "paired_items": len(merged),
            "mean_score_difference_model_a": merged["score_difference_a"].mean(),
            "mean_score_difference_model_b": merged["score_difference_b"].mean(),
            "mean_difference_a_minus_b": diff.mean(),
            "median_difference_a_minus_b": diff.median(),
            "wilcoxon_statistic": statistic,
            "wilcoxon_p_value": p_value,
            "significant_at_0_05": p_value < 0.05 if p_value is not None else False,
        })

    output_df = pd.DataFrame(rows)

    output_df.to_csv(
        OUTPUT_DIR / "pairwise_model_wilcoxon_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    required_columns = [
        "id",
        "model_name",
        "preferred_gender",
        "score_difference",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    overall_tests(df)

    for group_column in ["dialect", "dimension", "stereotype_direction"]:
        if group_column in df.columns:
            grouped_binomial_tests(df, group_column)

    pairwise_model_wilcoxon(df)

    print("Statistical tests completed.")
    print("Outputs saved to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()