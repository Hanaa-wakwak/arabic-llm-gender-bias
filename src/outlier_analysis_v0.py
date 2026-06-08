from pathlib import Path
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
RESULTS_DIR = Path("results")
INPUT_PATH = RESULTS_DIR / "scoring_results_v0.csv"

TOP_MASC_PATH = RESULTS_DIR / "top_masculine_outliers_v0.csv"
TOP_FEM_PATH = RESULTS_DIR / "top_feminine_outliers_v0.csv"
OUTLIER_SUMMARY_PATH = RESULTS_DIR / "outlier_summary_v0.csv"

# -----------------------------
# Load results
# -----------------------------
df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

print("=" * 70)
print("Outlier Analysis - Pilot Scoring Results")
print("=" * 70)

# -----------------------------
# Sort by score difference
# -----------------------------
# High positive = strong masculine preference
top_masculine = df.sort_values("score_difference", ascending=False).head(10)

# High negative = strong feminine preference
top_feminine = df.sort_values("score_difference", ascending=True).head(10)

# -----------------------------
# Add absolute difference
# -----------------------------
df["absolute_score_difference"] = df["score_difference"].abs()
top_absolute = df.sort_values("absolute_score_difference", ascending=False).head(10)

# -----------------------------
# Save files
# -----------------------------
top_masculine.to_csv(TOP_MASC_PATH, index=False, encoding="utf-8-sig")
top_feminine.to_csv(TOP_FEM_PATH, index=False, encoding="utf-8-sig")

outlier_summary = top_absolute[
    [
        "id",
        "dimension",
        "dialect",
        "stereotype_direction",
        "masculine_sentence",
        "feminine_sentence",
        "masculine_score",
        "feminine_score",
        "score_difference",
        "absolute_score_difference",
        "preferred_gender",
    ]
]

outlier_summary.to_csv(OUTLIER_SUMMARY_PATH, index=False, encoding="utf-8-sig")

# -----------------------------
# Print results
# -----------------------------
print("\nTop 10 masculine-preferred items:")
print(
    top_masculine[
        [
            "id",
            "dimension",
            "dialect",
            "stereotype_direction",
            "masculine_sentence",
            "feminine_sentence",
            "score_difference",
        ]
    ]
)

print("\nTop 10 feminine-preferred items:")
print(
    top_feminine[
        [
            "id",
            "dimension",
            "dialect",
            "stereotype_direction",
            "masculine_sentence",
            "feminine_sentence",
            "score_difference",
        ]
    ]
)

print("\nTop 10 strongest absolute outliers:")
print(outlier_summary)

print("\nSaved files:")
print(TOP_MASC_PATH)
print(TOP_FEM_PATH)
print(OUTLIER_SUMMARY_PATH)

print("\nDone.")