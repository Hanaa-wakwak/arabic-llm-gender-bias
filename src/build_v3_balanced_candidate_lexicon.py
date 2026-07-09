from pathlib import Path
import pandas as pd


V2_PATH = Path("data/occupational_benchmark/occupations_fields_v2.csv")
V3_PATH = Path("data/occupational_benchmark/occupations_fields_v3.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupations_fields_v3_balanced_candidate.csv")


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


def normalize_text(value):
    return str(value).strip().lower()


def make_pair_id(row):
    return (
        normalize_text(row["masculine_occupation"])
        + "|||"
        + normalize_text(row["feminine_occupation"])
    )


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    v2_df = pd.read_csv(V2_PATH, encoding="utf-8-sig")
    v3_df = pd.read_csv(V3_PATH, encoding="utf-8-sig")

    v2_df = normalize_columns(v2_df)
    v3_df = normalize_columns(v3_df)

    required = [
        "field",
        "masculine_occupation",
        "feminine_occupation",
        "stereotype_label",
    ]

    for name, df in [("v2", v2_df), ("v3", v3_df)]:
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(
                f"{name} missing required columns: {missing}\n"
                f"Available columns: {list(df.columns)}"
            )

    # Prepare v2 exact occupations as the core.
    v2_core = v2_df.copy()
    v2_core["source_version"] = "v2_preserved"
    v2_core["pair_id"] = v2_core.apply(make_pair_id, axis=1)

    # Prepare v3 additions only if not already in v2.
    v3_df["pair_id"] = v3_df.apply(make_pair_id, axis=1)
    v2_pairs = set(v2_core["pair_id"])

    v3_additions = v3_df[~v3_df["pair_id"].isin(v2_pairs)].copy()
    v3_additions["source_version"] = "v3_candidate_addition"

    # Keep controlled number of additions per stereotype label.
    # This is candidate only, not final validation.
    target_total = 90
    needed_additions = target_total - len(v2_core)

    if needed_additions < 0:
        raise ValueError("v2 already has more occupations than target_total.")

    # Select additions in a balanced way across stereotype labels where possible.
    selected_additions = []

    labels = ["male_stereotyped", "female_stereotyped", "neutral"]

    per_round = True

    while len(selected_additions) < needed_additions and per_round:
        per_round = False

        for label in labels:
            if len(selected_additions) >= needed_additions:
                break

            candidates = v3_additions[
                (v3_additions["stereotype_label"] == label)
                & (~v3_additions["pair_id"].isin([row["pair_id"] for row in selected_additions]))
            ]

            if not candidates.empty:
                selected_additions.append(candidates.iloc[0].to_dict())
                per_round = True

    selected_additions_df = pd.DataFrame(selected_additions)

    combined_df = pd.concat(
        [v2_core, selected_additions_df],
        ignore_index=True,
    )

    combined_df = combined_df.drop_duplicates(subset=["pair_id"]).copy()

    combined_df.insert(0, "candidate_occupation_id", range(1, len(combined_df) + 1))

    # Add occupation_key / occupation_en if missing.
    if "occupation_key" not in combined_df.columns:
        combined_df["occupation_key"] = combined_df.apply(
            lambda row: f"occ_{row['candidate_occupation_id']:03d}",
            axis=1,
        )

    if "occupation_en" not in combined_df.columns:
        combined_df["occupation_en"] = combined_df["occupation_key"]

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


if __name__ == "__main__":
    main()