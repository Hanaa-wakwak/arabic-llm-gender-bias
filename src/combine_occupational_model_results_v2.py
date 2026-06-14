from pathlib import Path
import pandas as pd


RESULTS_DIR = Path("results/occupational_benchmark_v2")
OUTPUT_DIR = RESULTS_DIR / "combined_analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILES = {
    "aubmindlab/aragpt2-base": RESULTS_DIR / "scoring_results_occupational_v1_aubmindlab_aragpt2_base.csv",
    "aubmindlab/aragpt2-medium": RESULTS_DIR / "scoring_results_occupational_v1_aubmindlab_aragpt2_medium.csv",
    "bigscience/bloom-560m": RESULTS_DIR / "scoring_results_occupational_v1_bigscience_bloom_560m.csv",
    "bigscience/bloom-1b1": RESULTS_DIR / "scoring_results_occupational_v1_bigscience_bloom_1b1.csv",
}


def model_family(model_name):
    if "aragpt2" in model_name.lower():
        return "Arabic-specific"
    if "bloom" in model_name.lower():
        return "Multilingual"
    return "Other"


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
    all_dfs = []

    for model_name, path in MODEL_FILES.items():
        if not path.exists():
            print(f"Missing file, skipping: {path}")
            continue

        df = pd.read_csv(path, encoding="utf-8-sig")
        df["model_name"] = model_name
        df["model_family"] = model_family(model_name)
        all_dfs.append(df)

    if not all_dfs:
        raise ValueError("No model result files were found.")

    combined_df = pd.concat(all_dfs, ignore_index=True)

    combined_df.to_csv(
        OUTPUT_DIR / "occupational_v2_all_model_scoring_results.csv",
        index=False,
        encoding="utf-8-sig",
    )

    outputs = {
        "overall_by_model.csv": ["model_name", "model_family"],
        "by_model_and_field.csv": ["model_name", "model_family", "field"],
        "by_model_and_dialect.csv": ["model_name", "model_family", "dialect"],
        "by_model_and_template.csv": ["model_name", "model_family", "template_id"],
        "by_model_and_stereotype.csv": ["model_name", "model_family", "stereotype_direction"],
        "by_model_and_occupation.csv": ["model_name", "model_family", "field", "occupation_id", "occupation_m", "occupation_f"],
        "overall_by_model_family.csv": ["model_family"],
        "by_family_and_field.csv": ["model_family", "field"],
        "by_family_and_dialect.csv": ["model_family", "dialect"],
    }

    for filename, group_cols in outputs.items():
        summary_df = summarize_group(combined_df, group_cols)
        summary_df.to_csv(
            OUTPUT_DIR / filename,
            index=False,
            encoding="utf-8-sig",
        )

    print("Combined occupational v2 model analysis completed.")
    print("Outputs saved to:")
    print(OUTPUT_DIR)

    print("\nOverall by model:")
    print(summarize_group(combined_df, ["model_name", "model_family"]))


if __name__ == "__main__":
    main()