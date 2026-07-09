from pathlib import Path
import pandas as pd


V2_PATH = Path("data/occupational_benchmark/occupations_fields_v2.csv")
V3_PATH = Path("data/occupational_benchmark/occupations_fields_v3.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupations_fields_v3_balanced_candidate.csv")

TARGET_TOTAL_OCCUPATIONS = 90
TARGET_LABEL_COUNTS = {
    "male_stereotyped": 30,
    "female_stereotyped": 30,
    "neutral": 30,
}


def normalize_text(value):
    return str(value).strip().lower()


def normalize_columns(df):
    rename_map = {
        "occupation_m": "masculine_occupation",
        "occupation_f": "feminine_occupation",
        "stereotype_direction": "stereotype_label",
    }

    for old_col, new_col in rename_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df[new_col] = df[old_col]

    return df


def normalize_stereotype_label(value):
    value = str(value).strip()

    label_map = {
        "male_stereotype": "male_stereotyped",
        "female_stereotype": "female_stereotyped",
        "male": "male_stereotyped",
        "female": "female_stereotyped",
        "neutral": "neutral",
        "male_stereotyped": "male_stereotyped",
        "female_stereotyped": "female_stereotyped",
    }

    if value not in label_map:
        raise ValueError(f"Unknown stereotype label: {value}")

    return label_map[value]


def make_pair_id(row):
    masculine = normalize_text(row["masculine_occupation"])
    feminine = normalize_text(row["feminine_occupation"])
    return f"{masculine}|||{feminine}"


def fill_missing_identity_columns(df):
    if "occupation_key" not in df.columns:
        df["occupation_key"] = ""

    if "occupation_en" not in df.columns:
        df["occupation_en"] = ""

    return df


def clean_identity_columns(df):
    df = df.copy()

    df["occupation_key"] = df["occupation_key"].fillna("").astype(str).str.strip()
    df["occupation_en"] = df["occupation_en"].fillna("").astype(str).str.strip()

    for idx, row in df.iterrows():
        if not row["occupation_key"]:
            df.at[idx, "occupation_key"] = f"v3balanced_occ_{idx + 1:03d}"

        if not row["occupation_en"]:
            df.at[idx, "occupation_en"] = df.at[idx, "occupation_key"]

    return df


def validate_input(df, name):
    required = [
        "field",
        "masculine_occupation",
        "feminine_occupation",
        "stereotype_label",
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"{name} missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )


def choose_balanced_additions(v2_core, v3_additions, needed_additions):
    selected_rows = []

    current_counts = v2_core["stereotype_label"].value_counts().to_dict()

    used_pairs = set(v2_core["pair_id"])

    v3_additions = v3_additions.copy()

    while len(selected_rows) < needed_additions:
        # Select the label with the largest deficit from the target.
        deficits = {}

        for label, target_count in TARGET_LABEL_COUNTS.items():
            current_count = current_counts.get(label, 0)
            deficits[label] = target_count - current_count

        labels_by_need = sorted(
            deficits.keys(),
            key=lambda label: deficits[label],
            reverse=True,
        )

        selected_this_round = False

        for label in labels_by_need:
            candidates = v3_additions[
                (v3_additions["stereotype_label"] == label)
                & (~v3_additions["pair_id"].isin(used_pairs))
            ]

            if not candidates.empty:
                row = candidates.iloc[0].to_dict()
                selected_rows.append(row)
                used_pairs.add(row["pair_id"])
                current_counts[label] = current_counts.get(label, 0) + 1
                selected_this_round = True
                break

        # Fallback if a specific label has no candidates left.
        if not selected_this_round:
            fallback_candidates = v3_additions[
                ~v3_additions["pair_id"].isin(used_pairs)
            ]

            if fallback_candidates.empty:
                break

            row = fallback_candidates.iloc[0].to_dict()
            selected_rows.append(row)
            used_pairs.add(row["pair_id"])

            label = row["stereotype_label"]
            current_counts[label] = current_counts.get(label, 0) + 1

    return pd.DataFrame(selected_rows)


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    v2_df = pd.read_csv(V2_PATH, encoding="utf-8-sig")
    v3_df = pd.read_csv(V3_PATH, encoding="utf-8-sig")

    v2_df = normalize_columns(v2_df)
    v3_df = normalize_columns(v3_df)

    validate_input(v2_df, "v2")
    validate_input(v3_df, "v3")

    v2_df = fill_missing_identity_columns(v2_df)
    v3_df = fill_missing_identity_columns(v3_df)

    v2_df["stereotype_label"] = v2_df["stereotype_label"].apply(
        normalize_stereotype_label
    )
    v3_df["stereotype_label"] = v3_df["stereotype_label"].apply(
        normalize_stereotype_label
    )

    v2_core = v2_df.copy()
    v2_core["source_version"] = "v2_preserved"
    v2_core["pair_id"] = v2_core.apply(make_pair_id, axis=1)

    v3_df["pair_id"] = v3_df.apply(make_pair_id, axis=1)

    v2_pairs = set(v2_core["pair_id"])

    v3_additions = v3_df[~v3_df["pair_id"].isin(v2_pairs)].copy()
    v3_additions["source_version"] = "v3_candidate_addition"

    needed_additions = TARGET_TOTAL_OCCUPATIONS - len(v2_core)

    if needed_additions < 0:
        raise ValueError(
            f"v2 has {len(v2_core)} occupations, which is greater than target "
            f"{TARGET_TOTAL_OCCUPATIONS}."
        )

    selected_additions_df = choose_balanced_additions(
        v2_core=v2_core,
        v3_additions=v3_additions,
        needed_additions=needed_additions,
    )

    combined_df = pd.concat(
        [v2_core, selected_additions_df],
        ignore_index=True,
    )

    combined_df = combined_df.drop_duplicates(subset=["pair_id"]).copy()

    if len(combined_df) != TARGET_TOTAL_OCCUPATIONS:
        raise ValueError(
            f"Expected {TARGET_TOTAL_OCCUPATIONS} occupations, found {len(combined_df)}"
        )

    combined_df.insert(
        0,
        "candidate_occupation_id",
        range(1, len(combined_df) + 1),
    )

    combined_df = clean_identity_columns(combined_df)

    output_cols = [
        "candidate_occupation_id",
        "field",
        "occupation_key",
        "occupation_en",
        "masculine_occupation",
        "feminine_occupation",
        "stereotype_label",
        "source_version",
        "pair_id",
    ]

    optional_cols = ["workplace", "occupation_id"]

    for col in optional_cols:
        if col in combined_df.columns and col not in output_cols:
            output_cols.append(col)

    combined_df = combined_df[output_cols]

    allowed_labels = {"male_stereotyped", "female_stereotyped", "neutral"}
    invalid_labels = set(combined_df["stereotype_label"]) - allowed_labels

    if invalid_labels:
        raise ValueError(f"Invalid labels after normalization: {invalid_labels}")

    combined_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Created v3 balanced candidate lexicon:")
    print(OUTPUT_PATH)
    print("Rows:", len(combined_df))

    print("\nSource counts:")
    print(combined_df["source_version"].value_counts())

    print("\nStereotype counts:")
    print(combined_df["stereotype_label"].value_counts())

    print("\nField counts:")
    print(combined_df["field"].value_counts().sort_index())

    print("\nPreview:")
    print(combined_df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()