from pathlib import Path
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
RESULTS_DIR = Path("results")
INPUT_PATH = RESULTS_DIR / "scoring_results_v01.csv"
SUMMARY_PATH = RESULTS_DIR / "analysis_summary_v01.csv"
DIALECT_PATH = RESULTS_DIR / "analysis_by_dialect_v01.csv"
DIMENSION_PATH = RESULTS_DIR / "analysis_by_dimension_v01.csv"
STEREOTYPE_PATH = RESULTS_DIR / "analysis_by_stereotype_v01.csv"
DETAILED_PATH = RESULTS_DIR / "analysis_detailed_groups_v01.csv"

# -----------------------------
# Load scoring results
# -----------------------------
df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

print("=" * 70)
print("Arabic LLM Gender Bias - Pilot Scoring Analysis")
print("=" * 70)

print("\nLoaded results:")
print(df.shape)

# -----------------------------
# Overall summary
# -----------------------------
total_items = len(df)

masculine_preferred = int((df["preferred_gender"] == "masculine").sum())
feminine_preferred = int((df["preferred_gender"] == "feminine").sum())
equal_preferred = int((df["preferred_gender"] == "equal").sum())

avg_score_difference = df["score_difference"].mean()
median_score_difference = df["score_difference"].median()

summary = pd.DataFrame([{
    "total_items": total_items,
    "masculine_preferred_count": masculine_preferred,
    "feminine_preferred_count": feminine_preferred,
    "equal_count": equal_preferred,
    "masculine_preferred_percent": masculine_preferred / total_items * 100,
    "feminine_preferred_percent": feminine_preferred / total_items * 100,
    "equal_percent": equal_preferred / total_items * 100,
    "average_score_difference": avg_score_difference,
    "median_score_difference": median_score_difference,
}])

# -----------------------------
# Helper function for grouped analysis
# -----------------------------
def group_analysis(group_col):
    grouped = (
        df.groupby(group_col)
        .agg(
            total_items=("id", "count"),
            average_score_difference=("score_difference", "mean"),
            median_score_difference=("score_difference", "median"),
            masculine_preferred_count=("preferred_gender", lambda x: (x == "masculine").sum()),
            feminine_preferred_count=("preferred_gender", lambda x: (x == "feminine").sum()),
            equal_count=("preferred_gender", lambda x: (x == "equal").sum()),
        )
        .reset_index()
    )

    grouped["masculine_preferred_percent"] = (
        grouped["masculine_preferred_count"] / grouped["total_items"] * 100
    )

    grouped["feminine_preferred_percent"] = (
        grouped["feminine_preferred_count"] / grouped["total_items"] * 100
    )

    return grouped


by_dialect = group_analysis("dialect")
by_dimension = group_analysis("dimension")
by_stereotype = group_analysis("stereotype_direction")

# Detailed group: dialect x dimension x stereotype_direction
detailed = (
    df.groupby(["dialect", "dimension", "stereotype_direction"])
    .agg(
        total_items=("id", "count"),
        average_score_difference=("score_difference", "mean"),
        median_score_difference=("score_difference", "median"),
        masculine_preferred_count=("preferred_gender", lambda x: (x == "masculine").sum()),
        feminine_preferred_count=("preferred_gender", lambda x: (x == "feminine").sum()),
        equal_count=("preferred_gender", lambda x: (x == "equal").sum()),
    )
    .reset_index()
)

detailed["masculine_preferred_percent"] = (
    detailed["masculine_preferred_count"] / detailed["total_items"] * 100
)

detailed["feminine_preferred_percent"] = (
    detailed["feminine_preferred_count"] / detailed["total_items"] * 100
)

# -----------------------------
# Save outputs
# -----------------------------
summary.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")
by_dialect.to_csv(DIALECT_PATH, index=False, encoding="utf-8-sig")
by_dimension.to_csv(DIMENSION_PATH, index=False, encoding="utf-8-sig")
by_stereotype.to_csv(STEREOTYPE_PATH, index=False, encoding="utf-8-sig")
detailed.to_csv(DETAILED_PATH, index=False, encoding="utf-8-sig")

# -----------------------------
# Print outputs
# -----------------------------
print("\nOverall summary:")
print(summary)

print("\nAnalysis by dialect:")
print(by_dialect)

print("\nAnalysis by dimension:")
print(by_dimension)

print("\nAnalysis by stereotype direction:")
print(by_stereotype)

print("\nDetailed analysis:")
print(detailed)

print("\nSaved files:")
print(SUMMARY_PATH)
print(DIALECT_PATH)
print(DIMENSION_PATH)
print(STEREOTYPE_PATH)
print(DETAILED_PATH)

print("\nDone.")