from pathlib import Path
import pandas as pd


INPUT_PATH = Path("results/occupational_benchmark_v1/scoring_results_occupational_v1_aragpt2_base.csv")
OUTPUT_DIR = Path("results/occupational_benchmark_v1/analysis_aragpt2_base")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def summarize_group(df, group_cols):
    rows = []

    for group_values, group_df in df.groupby(group_cols):
        if not isinstance(group_values, tuple):
            group_values = (group_values,)

        row = {}

        for col, value in zip(group_cols, group_values):
            row[col] = value

        total = len(group_df)
        masculine_count = int((group_df["preferred_gender"] == "masculine").sum())
        feminine_count = int((group_df["preferred_gender"] == "feminine").sum())
        equal_count = int((group_df["preferred_gender"] == "equal").sum())

        row.update({
            "total_items": total,
            "masculine_preferred_count": masculine_count,
            "feminine_preferred_count": feminine_count,
            "equal_count": equal_count,
            "masculine_preferred_percent": masculine_count / total * 100 if total else 0,
            "feminine_preferred_percent": feminine_count / total * 100 if total else 0,
            "equal_percent": equal_count / total * 100 if total else 0,
            "average_score_difference": group_df["score_difference"].mean(),
            "median_score_difference": group_df["score_difference"].median(),
            "min_score_difference": group_df["score_difference"].min(),
            "max_score_difference": group_df["score_difference"].max(),
        })

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    required_columns = [
        "field",
        "occupation_id",
        "occupation_m",
        "occupation_f",
        "dialect",
        "template_id",
        "stereotype_direction",
        "preferred_gender",
        "score_difference",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    outputs = {
        "summary_by_field.csv": ["field"],
        "summary_by_field_and_dialect.csv": ["field", "dialect"],
        "summary_by_field_and_template.csv": ["field", "template_id"],
        "summary_by_occupation.csv": ["field", "occupation_id", "occupation_m", "occupation_f"],
        "summary_by_dialect.csv": ["dialect"],
        "summary_by_template.csv": ["template_id"],
        "summary_by_stereotype_direction.csv": ["stereotype_direction"],
    }

    for filename, group_cols in outputs.items():
        summary_df = summarize_group(df, group_cols)
        summary_df.to_csv(OUTPUT_DIR / filename, index=False, encoding="utf-8-sig")

    print("Occupational analysis completed.")
    print("Outputs saved to:")
    print(OUTPUT_DIR)

    print("\nSummary by field:")
    print(summarize_group(df, ["field"]))


if __name__ == "__main__":
    main()