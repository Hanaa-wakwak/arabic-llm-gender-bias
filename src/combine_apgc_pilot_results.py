from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("results/external_datasets/apgc/combined_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


MODEL_FILES = {
    "aubmindlab/aragpt2-base": Path("results/external_datasets/apgc/scoring_results_occupational_v1_aubmindlab_aragpt2_base.csv"),
    "aubmindlab/aragpt2-medium": Path("results/external_datasets/apgc/scoring_results_occupational_v1_aubmindlab_aragpt2_medium.csv"),
    "bigscience/bloom-560m": Path("results/external_datasets/apgc/scoring_results_occupational_v1_bigscience_bloom_560m.csv"),
    "bigscience/bloom-1b1": Path("results/external_datasets/apgc/scoring_results_occupational_v1_bigscience_bloom_1b1.csv"),
    "facebook/xglm-564M": Path("results/external_datasets/apgc/scoring_results_occupational_v1_facebook_xglm_564M.csv"),
    "Qwen/Qwen2.5-0.5B": Path("results/external_datasets/apgc/scoring_results_occupational_v1_Qwen_Qwen2_5_0_5B.csv"),
}


def model_family(model_name):
    if "aragpt2" in model_name.lower():
        return "Arabic-specific"
    return "Non-Arabic-specific"


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
    missing_files = []

    for model_name, path in MODEL_FILES.items():
        if not path.exists():
            missing_files.append(str(path))
            continue

        df = pd.read_csv(path, encoding="utf-8-sig")
        df["model_name"] = model_name
        df["model_family"] = model_family(model_name)
        all_dfs.append(df)

    if missing_files:
        print("Warning: missing files:")
        for path in missing_files:
            print(path)

    if not all_dfs:
        raise ValueError("No APGC scoring files found.")

    combined_df = pd.concat(all_dfs, ignore_index=True)

    combined_df.to_csv(
        OUTPUT_DIR / "apgc_pilot_all_model_scoring_results.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summarize_group(combined_df, ["model_name", "model_family"]).to_csv(
        OUTPUT_DIR / "apgc_pilot_overall_by_model.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summarize_group(combined_df, ["model_family"]).to_csv(
        OUTPUT_DIR / "apgc_pilot_overall_by_model_family.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summarize_group(combined_df, ["model_name", "model_family", "gender_context"]).to_csv(
        OUTPUT_DIR / "apgc_pilot_by_model_and_gender_context.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("APGC pilot combined analysis completed.")
    print("Outputs saved to:", OUTPUT_DIR)

    print("\nOverall by model:")
    print(summarize_group(combined_df, ["model_name", "model_family"]))


if __name__ == "__main__":
    main()