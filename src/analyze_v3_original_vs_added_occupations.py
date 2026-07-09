from pathlib import Path
import argparse
import pandas as pd


V2_OCCUPATIONS_PATH = Path("data/occupational_benchmark/occupations_fields_v2.csv")


def normalize_text(value):
    return str(value).strip().lower()


def normalize_columns(df):
    """
    Normalize old and new occupation column names.

    v2 old names:
    occupation_m, occupation_f, stereotype_direction

    v3 new names:
    masculine_occupation, feminine_occupation, stereotype_label
    """

    rename_map = {
        "occupation_m": "masculine_occupation",
        "occupation_f": "feminine_occupation",
        "stereotype_direction": "stereotype_label",
    }

    for old_col, new_col in rename_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df[new_col] = df[old_col]

    return df


def make_pair_identifier(row):
    masculine = normalize_text(row["masculine_occupation"])
    feminine = normalize_text(row["feminine_occupation"])
    return f"{masculine}|||{feminine}"


def summarize_group(df, group_cols):
    rows = []

    for group_values, group_df in df.groupby(group_cols, dropna=False):
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
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Scored v3 or v3_controlled occupational CSV.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory to save diagnostic outputs.",
    )

    parser.add_argument(
        "--v2_occupations",
        default=str(V2_OCCUPATIONS_PATH),
        help="Path to v2 occupations file.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    v2_path = Path(args.v2_occupations)

    output_dir.mkdir(parents=True, exist_ok=True)

    scored_df = pd.read_csv(input_path, encoding="utf-8-sig")
    v2_occ_df = pd.read_csv(v2_path, encoding="utf-8-sig")

    scored_df = normalize_columns(scored_df)
    v2_occ_df = normalize_columns(v2_occ_df)

    required_scored_columns = [
        "model_name",
        "preferred_gender",
        "score_difference",
        "field",
        "template_id",
        "masculine_occupation",
        "feminine_occupation",
    ]

    missing_scored = [
        col for col in required_scored_columns
        if col not in scored_df.columns
    ]

    if missing_scored:
        raise ValueError(
            f"Scored file missing required columns: {missing_scored}\n"
            f"Available scored columns: {list(scored_df.columns)}"
        )

    required_v2_columns = [
        "masculine_occupation",
        "feminine_occupation",
    ]

    missing_v2 = [
        col for col in required_v2_columns
        if col not in v2_occ_df.columns
    ]

    if missing_v2:
        raise ValueError(
            f"v2 occupations file missing required columns after normalization: {missing_v2}\n"
            f"Available v2 columns: {list(v2_occ_df.columns)}"
        )

    scored_df["occupation_pair_identifier"] = scored_df.apply(
        make_pair_identifier,
        axis=1,
    )

    v2_occ_df["occupation_pair_identifier"] = v2_occ_df.apply(
        make_pair_identifier,
        axis=1,
    )

    v2_pairs = set(v2_occ_df["occupation_pair_identifier"])

    scored_df["occupation_origin"] = scored_df["occupation_pair_identifier"].apply(
        lambda pair: "original_v2_occupation" if pair in v2_pairs else "added_v3_occupation"
    )

    if "occupation_key" not in scored_df.columns:
        scored_df["occupation_key"] = scored_df["occupation_pair_identifier"]

    if "occupation_en" not in scored_df.columns:
        scored_df["occupation_en"] = scored_df["occupation_key"]

    summary_by_origin = summarize_group(
        scored_df,
        ["model_name", "occupation_origin"],
    )

    summary_by_origin_and_template = summarize_group(
        scored_df,
        ["model_name", "occupation_origin", "template_id"],
    )

    summary_by_origin_and_field = summarize_group(
        scored_df,
        ["model_name", "occupation_origin", "field"],
    )

    occupation_level = summarize_group(
        scored_df,
        [
            "model_name",
            "occupation_origin",
            "field",
            "occupation_key",
            "occupation_en",
            "masculine_occupation",
            "feminine_occupation",
        ],
    )

    occupation_level_sorted_feminine = occupation_level.sort_values(
        "average_score_difference",
        ascending=True,
    )

    occupation_level_sorted_masculine = occupation_level.sort_values(
        "average_score_difference",
        ascending=False,
    )

    metadata_df = pd.DataFrame([
        {
            "input_file": str(input_path),
            "v2_occupations_file": str(v2_path),
            "comparison_method": "masculine_occupation + feminine_occupation pair",
            "v2_unique_occupation_pairs": len(v2_pairs),
            "scored_unique_occupation_pairs": scored_df["occupation_pair_identifier"].nunique(),
            "original_v2_pairs_found_in_scored_file": scored_df[
                scored_df["occupation_origin"] == "original_v2_occupation"
            ]["occupation_pair_identifier"].nunique(),
            "added_v3_pairs_found_in_scored_file": scored_df[
                scored_df["occupation_origin"] == "added_v3_occupation"
            ]["occupation_pair_identifier"].nunique(),
        }
    ])

    scored_df.to_csv(
        output_dir / "scored_with_occupation_origin.csv",
        index=False,
        encoding="utf-8-sig",
    )

    metadata_df.to_csv(
        output_dir / "diagnostic_metadata.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_by_origin.to_csv(
        output_dir / "summary_by_occupation_origin.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_by_origin_and_template.to_csv(
        output_dir / "summary_by_occupation_origin_and_template.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_by_origin_and_field.to_csv(
        output_dir / "summary_by_occupation_origin_and_field.csv",
        index=False,
        encoding="utf-8-sig",
    )

    occupation_level.to_csv(
        output_dir / "summary_by_occupation.csv",
        index=False,
        encoding="utf-8-sig",
    )

    occupation_level_sorted_feminine.head(20).to_csv(
        output_dir / "top_20_feminine_driving_occupations.csv",
        index=False,
        encoding="utf-8-sig",
    )

    occupation_level_sorted_masculine.head(20).to_csv(
        output_dir / "top_20_masculine_driving_occupations.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v3 original-vs-added occupation diagnostic completed.")
    print("Input:", input_path)
    print("V2 occupations:", v2_path)
    print("Output:", output_dir)

    print("\nIdentifier metadata:")
    print(metadata_df.to_string(index=False))

    print("\nSummary by occupation origin:")
    print(summary_by_origin.to_string(index=False))

    print("\nTop feminine-driving occupations:")
    print(occupation_level_sorted_feminine.head(10).to_string(index=False))

    print("\nTop masculine-driving occupations:")
    print(occupation_level_sorted_masculine.head(10).to_string(index=False))


if __name__ == "__main__":
    main()