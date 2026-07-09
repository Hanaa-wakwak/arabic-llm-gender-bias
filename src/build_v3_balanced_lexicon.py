from pathlib import Path
import pandas as pd


CANDIDATE_PATH = Path("data/occupational_benchmark/occupations_fields_v3_balanced_candidate.csv")
SUPPLEMENT_PATH = Path("data/occupational_benchmark/female_stereotyped_supplement_v1.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupations_fields_v3_balanced.csv")

TARGET_COUNTS = {
    "male_stereotyped": 30,
    "female_stereotyped": 30,
    "neutral": 30,
}


def normalize_text(value):
    return str(value).strip().lower()


def make_pair_id(row):
    return (
        normalize_text(row["masculine_occupation"])
        + "|||"
        + normalize_text(row["feminine_occupation"])
    )


def normalize_stereotype_label(value):
    value = str(value).strip()

    label_map = {
        "male_stereotype": "male_stereotyped",
        "female_stereotype": "female_stereotyped",
        "male_stereotyped": "male_stereotyped",
        "female_stereotyped": "female_stereotyped",
        "neutral": "neutral",
    }

    if value not in label_map:
        raise ValueError(f"Unknown stereotype label: {value}")

    return label_map[value]


def ensure_columns(df):
    if "occupation_key" not in df.columns:
        df["occupation_key"] = ""

    if "occupation_en" not in df.columns:
        df["occupation_en"] = ""

    if "source_version" not in df.columns:
        df["source_version"] = "unknown_source"

    if "workplace" not in df.columns:
        df["workplace"] = ""

    return df


def clean_identity(df):
    df = df.copy()

    df["occupation_key"] = df["occupation_key"].fillna("").astype(str).str.strip()
    df["occupation_en"] = df["occupation_en"].fillna("").astype(str).str.strip()

    for idx, row in df.iterrows():
        if not row["occupation_key"]:
            df.at[idx, "occupation_key"] = f"balanced_occ_{idx + 1:03d}"

        if not row["occupation_en"]:
            df.at[idx, "occupation_en"] = df.at[idx, "occupation_key"]

    return df


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    candidate_df = pd.read_csv(CANDIDATE_PATH, encoding="utf-8-sig")
    supplement_df = pd.read_csv(SUPPLEMENT_PATH, encoding="utf-8-sig")

    candidate_df = ensure_columns(candidate_df)
    supplement_df = ensure_columns(supplement_df)

    candidate_df["stereotype_label"] = candidate_df["stereotype_label"].apply(
        normalize_stereotype_label
    )
    supplement_df["stereotype_label"] = supplement_df["stereotype_label"].apply(
        normalize_stereotype_label
    )

    candidate_df["pair_id"] = candidate_df.apply(make_pair_id, axis=1)
    supplement_df["pair_id"] = supplement_df.apply(make_pair_id, axis=1)

    # Mark supplement source clearly.
    supplement_df["source_version"] = "manual_female_stereotype_supplement"

    all_df = pd.concat(
        [candidate_df, supplement_df],
        ignore_index=True,
    )

    all_df = all_df.drop_duplicates(subset=["pair_id"]).copy()
    all_df = clean_identity(all_df)

    selected_parts = []

    for label, target_count in TARGET_COUNTS.items():
        label_df = all_df[all_df["stereotype_label"] == label].copy()

        if len(label_df) < target_count:
            raise ValueError(
                f"Not enough occupations for {label}. "
                f"Needed {target_count}, found {len(label_df)}"
            )

        # Prefer v2 preserved first, then v3 additions, then manual supplement.
        source_priority = {
            "v2_preserved": 0,
            "v3_candidate_addition": 1,
            "manual_female_stereotype_supplement": 2,
        }

        label_df["source_priority"] = label_df["source_version"].map(
            source_priority
        ).fillna(99)

        label_df = label_df.sort_values(
            by=["source_priority", "field", "occupation_key"],
            ascending=True,
        )

        selected_parts.append(label_df.head(target_count))

    balanced_df = pd.concat(selected_parts, ignore_index=True)

    balanced_df = balanced_df.drop(columns=["source_priority"], errors="ignore")

    balanced_df.insert(0, "balanced_occupation_id", range(1, len(balanced_df) + 1))

    output_cols = [
        "balanced_occupation_id",
        "field",
        "occupation_key",
        "occupation_en",
        "masculine_occupation",
        "feminine_occupation",
        "stereotype_label",
        "source_version",
        "pair_id",
        "workplace",
    ]

    balanced_df = balanced_df[output_cols]

    if len(balanced_df) != 90:
        raise ValueError(f"Expected 90 occupations, found {len(balanced_df)}")

    counts = balanced_df["stereotype_label"].value_counts().to_dict()

    for label, target_count in TARGET_COUNTS.items():
        if counts.get(label, 0) != target_count:
            raise ValueError(f"Expected {target_count} {label}, found {counts.get(label, 0)}")

    balanced_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Created true v3 balanced lexicon:")
    print(OUTPUT_PATH)
    print("Rows:", len(balanced_df))

    print("\nStereotype counts:")
    print(balanced_df["stereotype_label"].value_counts())

    print("\nSource counts:")
    print(balanced_df["source_version"].value_counts())

    print("\nField counts:")
    print(balanced_df["field"].value_counts().sort_index())


if __name__ == "__main__":
    main()