from pathlib import Path
import pandas as pd


INPUT_DIR = Path("results/model_comparison_v07")
OUTPUT_PATH = INPUT_DIR / "scoring_results_v07_all_models.csv"


def main():
    csv_files = sorted(INPUT_DIR.glob("scoring_results_v07_*.csv"))

    csv_files = [
        path for path in csv_files
        if path.name != "scoring_results_v07_all_models.csv"
    ]

    if not csv_files:
        raise FileNotFoundError("No individual model scoring files found.")

    all_dfs = []

    print("Files found:")
    for path in csv_files:
        print(path)
        df = pd.read_csv(path, encoding="utf-8-sig")
        all_dfs.append(df)

    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("\nCombined file saved to:")
    print(OUTPUT_PATH)

    print("\nModels included:")
    print(combined_df["model_name"].value_counts())


if __name__ == "__main__":
    main()