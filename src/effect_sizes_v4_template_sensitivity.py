from pathlib import Path
import argparse
import math
import pandas as pd
from scipy.stats import chi2_contingency


VARIABLES = [
    "model_name",
    "model_family",
    "template_id",
    "semantic_frame",
    "dialect",
    "stereotype_label",
    "field",
]


MODEL_FAMILY_MAP = {
    "aubmindlab/aragpt2-base": "Arabic-specific",
    "aubmindlab/aragpt2-medium": "Arabic-specific",
    "bigscience/bloom-560m": "Non-Arabic-specific",
    "bigscience/bloom-1b1": "Non-Arabic-specific",
    "facebook/xglm-564M": "Non-Arabic-specific",
    "Qwen/Qwen2.5-0.5B": "Non-Arabic-specific",
}


def cramers_v(confusion_matrix):
    chi2, p, dof, expected = chi2_contingency(confusion_matrix)

    n = confusion_matrix.to_numpy().sum()

    if n == 0:
        return None, chi2, p, dof

    rows, cols = confusion_matrix.shape

    denominator = n * (min(rows - 1, cols - 1))

    if denominator == 0:
        return None, chi2, p, dof

    v = math.sqrt(chi2 / denominator)

    return v, chi2, p, dof


def interpret_cramers_v(value):
    if value is None:
        return "not_applicable"

    if value < 0.1:
        return "very_small"
    elif value < 0.3:
        return "small"
    elif value < 0.5:
        return "medium"
    else:
        return "large"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="combined_v4_scored_results.csv",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory for effect-size outputs.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    if "model_family" not in df.columns:
        df["model_family"] = df["model_name"].map(MODEL_FAMILY_MAP).fillna("Unknown")

    df = df[df["preferred_gender"].isin(["masculine", "feminine"])].copy()

    rows = []

    for variable in VARIABLES:
        if variable not in df.columns:
            continue

        table = pd.crosstab(df[variable], df["preferred_gender"])

        if table.shape[0] < 2 or table.shape[1] < 2:
            rows.append({
                "variable": variable,
                "levels": table.shape[0],
                "chi2": None,
                "p_value": None,
                "degrees_of_freedom": None,
                "cramers_v": None,
                "effect_size_interpretation": "not_applicable",
                "note": "insufficient table size",
            })
            continue

        v, chi2, p, dof = cramers_v(table)

        rows.append({
            "variable": variable,
            "levels": table.shape[0],
            "chi2": chi2,
            "p_value": p,
            "degrees_of_freedom": dof,
            "cramers_v": v,
            "effect_size_interpretation": interpret_cramers_v(v),
            "note": "ok",
        })

    results_df = pd.DataFrame(rows)

    results_df = results_df.sort_values(
        by="cramers_v",
        ascending=False,
        na_position="last",
    )

    results_df.to_csv(
        output_dir / "v4_cramers_v_effect_sizes.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v4 effect-size analysis completed.")
    print("Input:", input_path)
    print("Output:", output_dir)

    print("\nEffect sizes:")
    print(results_df.to_string(index=False))


if __name__ == "__main__":
    main()