from pathlib import Path
from itertools import combinations

import argparse
import pandas as pd
from scipy.stats import binomtest, wilcoxon, chi2_contingency


def bonferroni_correction(p_values):
    m = len(p_values)
    return [min(p * m, 1.0) for p in p_values]


def holm_correction(p_values):
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted = [None] * m
    running_max = 0

    for rank, (original_idx, p) in enumerate(indexed):
        corrected = min((m - rank) * p, 1.0)
        running_max = max(running_max, corrected)
        adjusted[original_idx] = min(running_max, 1.0)

    return adjusted


def benjamini_hochberg_correction(p_values):
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1], reverse=True)
    adjusted = [None] * m
    running_min = 1.0

    for rank_from_largest, (original_idx, p) in enumerate(indexed):
        rank = m - rank_from_largest
        corrected = min((p * m) / rank, 1.0)
        running_min = min(running_min, corrected)
        adjusted[original_idx] = running_min

    return adjusted


def run_binomial(group_df, group_info):
    masculine_count = int((group_df["preferred_gender"] == "masculine").sum())
    feminine_count = int((group_df["preferred_gender"] == "feminine").sum())
    equal_count = int((group_df["preferred_gender"] == "equal").sum())

    tested_total = masculine_count + feminine_count

    if tested_total > 0:
        p_value = binomtest(
            k=masculine_count,
            n=tested_total,
            p=0.5,
            alternative="two-sided",
        ).pvalue
    else:
        p_value = None

    if masculine_count > feminine_count:
        direction = "masculine"
    elif feminine_count > masculine_count:
        direction = "feminine"
    else:
        direction = "balanced"

    return {
        **group_info,
        "total_items": len(group_df),
        "tested_items_excluding_equal": tested_total,
        "masculine_preferred_count": masculine_count,
        "feminine_preferred_count": feminine_count,
        "equal_count": equal_count,
        "masculine_preferred_percent": masculine_count / len(group_df) * 100 if len(group_df) else 0,
        "feminine_preferred_percent": feminine_count / len(group_df) * 100 if len(group_df) else 0,
        "preference_direction": direction,
        "binomial_p_value": p_value,
        "significant_at_0_05": p_value < 0.05 if p_value is not None else False,
    }


def binomial_by_group(df, group_cols, output_dir, filename):
    rows = []

    for group_values, group_df in df.groupby(group_cols):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        group_info = {}

        for col, value in zip(group_cols, group_values):
            group_info[col] = value

        rows.append(run_binomial(group_df, group_info))

    pd.DataFrame(rows).to_csv(
        output_dir / filename,
        index=False,
        encoding="utf-8-sig",
    )


def wilcoxon_by_model(df, output_dir):
    rows = []

    for model_name, model_df in df.groupby("model_name"):
        scores = model_df["score_difference"].dropna()

        try:
            result = wilcoxon(scores)
            statistic = result.statistic
            p_value = result.pvalue
        except ValueError:
            statistic = None
            p_value = None

        rows.append({
            "model_name": model_name,
            "model_family": model_df["model_family"].iloc[0],
            "total_items": len(scores),
            "average_score_difference": scores.mean(),
            "median_score_difference": scores.median(),
            "wilcoxon_statistic": statistic,
            "wilcoxon_p_value": p_value,
            "significant_at_0_05": p_value < 0.05 if p_value is not None else False,
        })

    pd.DataFrame(rows).to_csv(
        output_dir / "overall_wilcoxon_by_model.csv",
        index=False,
        encoding="utf-8-sig",
    )


def pairwise_model_wilcoxon(df, output_dir):
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
        })

    output_df = pd.DataFrame(rows)

    p_values = output_df["wilcoxon_p_value"].tolist()

    output_df["p_bonferroni"] = bonferroni_correction(p_values)
    output_df["p_holm"] = holm_correction(p_values)
    output_df["p_bh_fdr"] = benjamini_hochberg_correction(p_values)

    output_df["significant_uncorrected_0_05"] = output_df["wilcoxon_p_value"] < 0.05
    output_df["significant_bonferroni_0_05"] = output_df["p_bonferroni"] < 0.05
    output_df["significant_holm_0_05"] = output_df["p_holm"] < 0.05
    output_df["significant_bh_fdr_0_05"] = output_df["p_bh_fdr"] < 0.05

    output_df.to_csv(
        output_dir / "pairwise_model_wilcoxon_corrected.csv",
        index=False,
        encoding="utf-8-sig",
    )


def chi_square_family_preference(df, output_dir):
    table = pd.crosstab(df["model_family"], df["preferred_gender"])

    for col in ["masculine", "feminine"]:
        if col not in table.columns:
            table[col] = 0

    tested_table = table[["masculine", "feminine"]]

    chi2, p_value, dof, expected = chi2_contingency(tested_table)

    pd.DataFrame([{
        "test": "chi_square_model_family_vs_preference",
        "chi2": chi2,
        "p_value": p_value,
        "degrees_of_freedom": dof,
        "significant_at_0_05": p_value < 0.05,
    }]).to_csv(
        output_dir / "chi_square_model_family_preference.csv",
        index=False,
        encoding="utf-8-sig",
    )

    tested_table.to_csv(
        output_dir / "model_family_preference_contingency_table.csv",
        encoding="utf-8-sig",
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Combined all-model scoring CSV.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Output directory for statistical tests.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "id",
        "model_name",
        "model_family",
        "field",
        "dialect",
        "template_id",
        "preferred_gender",
        "score_difference",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    binomial_by_group(
        df,
        ["model_name", "model_family"],
        output_dir,
        "overall_binomial_by_model.csv",
    )

    binomial_by_group(
        df,
        ["model_name", "model_family", "field"],
        output_dir,
        "binomial_by_model_and_field.csv",
    )

    binomial_by_group(
        df,
        ["model_name", "model_family", "dialect"],
        output_dir,
        "binomial_by_model_and_dialect.csv",
    )

    binomial_by_group(
        df,
        ["model_family"],
        output_dir,
        "binomial_by_model_family.csv",
    )

    binomial_by_group(
        df,
        ["model_family", "field"],
        output_dir,
        "binomial_by_family_and_field.csv",
    )

    wilcoxon_by_model(df, output_dir)
    pairwise_model_wilcoxon(df, output_dir)
    chi_square_family_preference(df, output_dir)

    print("Occupational statistical testing completed.")
    print("Input:", input_path)
    print("Outputs saved to:", output_dir)


if __name__ == "__main__":
    main()