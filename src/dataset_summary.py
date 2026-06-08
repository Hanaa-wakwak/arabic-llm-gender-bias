import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/benchmark_v0/minimal_pairs_v0.csv")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

summary = {
    "total_rows": len(df),
    "total_columns": len(df.columns),
    "msa_items": int((df["dialect"] == "MSA").sum()),
    "egyptian_items": int((df["dialect"] == "Egyptian").sum()),
    "occupation_items": int((df["dimension"] == "occupation").sum()),
    "trait_items": int((df["dimension"] == "trait").sum()),
    "male_stereotype_items": int((df["stereotype_direction"] == "male_stereotype").sum()),
    "female_stereotype_items": int((df["stereotype_direction"] == "female_stereotype").sum()),
    "neutral_items": int((df["stereotype_direction"] == "neutral").sum()),
}

summary_df = pd.DataFrame([summary])

output_path = RESULTS_DIR / "dataset_summary_v0.csv"
summary_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("Dataset summary saved to:")
print(output_path)

print("\nSummary:")
print(summary_df)