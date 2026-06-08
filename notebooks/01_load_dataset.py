import pandas as pd
from pathlib import Path

# Path to the pilot benchmark file
DATA_PATH = Path("data/benchmark_v0/minimal_pairs_v0.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("Arabic LLM Gender Bias - Pilot Dataset Check")
print("=" * 60)

# Basic shape
print("\nDataset shape:")
print(df.shape)

# Column names
print("\nColumns:")
print(df.columns.tolist())

# First rows
print("\nFirst 5 rows:")
print(df.head())

# Count by dialect
print("\nCount by dialect:")
print(df["dialect"].value_counts())

# Count by dimension
print("\nCount by dimension:")
print(df["dimension"].value_counts())

# Count by stereotype direction
print("\nCount by stereotype direction:")
print(df["stereotype_direction"].value_counts())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Basic validation
expected_columns = [
    "id",
    "dimension",
    "dialect",
    "masculine_sentence",
    "feminine_sentence",
    "stereotype_direction",
    "notes"
]

missing_columns = [col for col in expected_columns if col not in df.columns]

print("\nValidation result:")
if missing_columns:
    print("Missing columns:", missing_columns)
else:
    print("All expected columns exist.")

if len(df) == 50:
    print("Dataset contains 50 rows.")
else:
    print(f"Dataset contains {len(df)} rows, expected 50.")

print("\nDone.")