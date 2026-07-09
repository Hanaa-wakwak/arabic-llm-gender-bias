from pathlib import Path
import argparse
import pandas as pd
from scipy.stats import chi2_contingency


MODEL_FAMILY_MAP = {
    "aubmindlab/aragpt2-base": "Arabic-specific",
    "aubmindlab/aragpt2-medium": "Arabic-specific",
    "bigscience/bloom-560m": "Non-Arabic-specific",
    "bigscience/bloom-1b1": "Non-Arabic-specific",
    "facebook/xglm-564M": "Non-Arabic-specific",
    "Qwen/Qwen2.5-0.5B": "Non-Arabic-specific",
}


def run_chi_square(df, row_col, col_col, label):
    filtered = df[df[col_col].isin(["masculine", "feminine"])].copy()

    table = pd.crosstab(filtered[row_col], filtered[col_col])

    if table.shape[0] < 2 or table.shape[1] < 2:
        return {
            "test_label": label,
            "row_variable": row_col,
            "column_variable": col_col,
            "chi2": None,
            "p_value": None,
            "degrees_of_freedom": None,
            "significant_p_lt_0_05": None,
            "note": "insufficient table size",
        }

    chi2, p, dof, expected = chi2_contingency(table)

    return {
        "test_label": label,
        "row_variable": row_col,
        "column_variable": col_col,
        "chi2": chi2,
        "p_value": p,
        "degrees_of_freedom": dof,
        "significant_p_lt_0_05": p < 0.05,
        "note": "ok",
    }


def run_grouped_chi_square(df, group_col, row_col, col_col):
    rows = []

    for group_value, group_df in df.groupby(group_col):
        result = run_chi_square(
            group_df,
            row_col=row_col,
            col_col=col_col,
            label=f"{group_col}={group_value}",
        )
        result[group_col] = group_value
        rows.append(result)

    return pd.DataFrame(rows)


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
        help="Output directory for v4 statistical tests.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required = [
        "model_name",
        "preferred_gender",
        "template_id",
        "semantic_frame",
        "dialect",
        "stereotype_label",
        "field",
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    df["model_family"] = df["model_name"].map(MODEL_FAMILY_MAP).fillna("Unknown")

    overall_tests = [
        run_chi_square(
            df,
            row_col="model_name",
            col_col="preferred_gender",
            label="model_name_vs_preferred_gender",
        ),
        run_chi_square(
            df,
            row_col="model_family",
            col_col="preferred_gender",
            label="model_family_vs_preferred_gender",
        ),
        run_chi_square(
            df,
            row_col="template_id",
            col_col="preferred_gender",
            label="template_id_vs_preferred_gender",
        ),
        run_chi_square(
            df,
            row_col="semantic_frame",
            col_col="preferred_gender",
            label="semantic_frame_vs_preferred_gender",
        ),
        run_chi_square(
            df,
            row_col="dialect",
            col_col="preferred_gender",
            label="dialect_vs_preferred_gender",
        ),
        run_chi_square(
            df,
            row_col="stereotype_label",
            col_col="preferred_gender",
            label="stereotype_label_vs_preferred_gender",
        ),
        run_chi_square(
            df,
            row_col="field",
            col_col="preferred_gender",
            label="field_vs_preferred_gender",
        ),
    ]

    overall_tests_df = pd.DataFrame(overall_tests)

    template_family_tests = run_grouped_chi_square(
        df,
        group_col="template_id",
        row_col="model_family",
        col_col="preferred_gender",
    )

    semantic_family_tests = run_grouped_chi_square(
        df,
        group_col="semantic_frame",
        row_col="model_family",
        col_col="preferred_gender",
    )

    dialect_family_tests = run_grouped_chi_square(
        df,
        group_col="dialect",
        row_col="model_family",
        col_col="preferred_gender",
    )

    model_template_tests = run_grouped_chi_square(
        df,
        group_col="model_name",
        row_col="template_id",
        col_col="preferred_gender",
    )

    model_semantic_tests = run_grouped_chi_square(
        df,
        group_col="model_name",
        row_col="semantic_frame",
        col_col="preferred_gender",
    )

    df.to_csv(
        output_dir / "combined_v4_scored_results_with_family.csv",
        index=False,
        encoding="utf-8-sig",
    )

    overall_tests_df.to_csv(
        output_dir / "v4_overall_chi_square_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )

    template_family_tests.to_csv(
        output_dir / "v4_template_model_family_chi_square_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )

    semantic_family_tests.to_csv(
        output_dir / "v4_semantic_frame_model_family_chi_square_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )

    dialect_family_tests.to_csv(
        output_dir / "v4_dialect_model_family_chi_square_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )

    model_template_tests.to_csv(
        output_dir / "v4_model_template_chi_square_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )

    model_semantic_tests.to_csv(
        output_dir / "v4_model_semantic_frame_chi_square_tests.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v4 statistical tests completed.")
    print("Input:", input_path)
    print("Output:", output_dir)

    print("\nOverall tests:")
    print(overall_tests_df.to_string(index=False))


if __name__ == "__main__":
    main()