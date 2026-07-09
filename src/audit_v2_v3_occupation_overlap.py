from pathlib import Path
import pandas as pd


V2_PATH = Path("data/occupational_benchmark/occupations_fields_v2.csv")
V3_PATH = Path("data/occupational_benchmark/occupations_fields_v3.csv")
OUTPUT_DIR = Path("results/occupational_benchmark_v3_diagnostics/occupation_overlap_audit")


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
    masculine = normalize_text(row["masculine_occupation"])
    feminine = normalize_text(row["feminine_occupation"])
    return f"{masculine}|||{feminine}"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    v2_df = pd.read_csv(V2_PATH, encoding="utf-8-sig")
    v3_df = pd.read_csv(V3_PATH, encoding="utf-8-sig")

    v2_df = normalize_columns(v2_df)
    v3_df = normalize_columns(v3_df)

    required = ["field", "masculine_occupation", "feminine_occupation"]

    for name, df in [("v2", v2_df), ("v3", v3_df)]:
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(
                f"{name} missing columns: {missing}\n"
                f"Available columns: {list(df.columns)}"
            )

    v2_df["pair_id"] = v2_df.apply(make_pair_id, axis=1)
    v3_df["pair_id"] = v3_df.apply(make_pair_id, axis=1)

    v2_pairs = set(v2_df["pair_id"])
    v3_pairs = set(v3_df["pair_id"])

    exact_matches = v2_df[v2_df["pair_id"].isin(v3_pairs)].copy()
    missing_from_v3 = v2_df[~v2_df["pair_id"].isin(v3_pairs)].copy()
    added_in_v3 = v3_df[~v3_df["pair_id"].isin(v2_pairs)].copy()

    exact_matches["overlap_status"] = "exact_match_in_v3"
    missing_from_v3["overlap_status"] = "v2_missing_from_v3"
    added_in_v3["overlap_status"] = "added_or_changed_in_v3"

    # Field-level summary
    summary_rows = [
        {
            "metric": "v2_total_occupations",
            "value": len(v2_df),
        },
        {
            "metric": "v3_total_occupations",
            "value": len(v3_df),
        },
        {
            "metric": "exact_v2_pairs_found_in_v3",
            "value": len(exact_matches),
        },
        {
            "metric": "v2_pairs_missing_from_v3",
            "value": len(missing_from_v3),
        },
        {
            "metric": "v3_pairs_not_exactly_in_v2",
            "value": len(added_in_v3),
        },
    ]

    summary_df = pd.DataFrame(summary_rows)

    field_summary = []

    for field in sorted(set(v2_df["field"]).union(set(v3_df["field"]))):
        v2_field = v2_df[v2_df["field"] == field]
        v3_field = v3_df[v3_df["field"] == field]
        match_field = exact_matches[exact_matches["field"] == field]
        missing_field = missing_from_v3[missing_from_v3["field"] == field]
        added_field = added_in_v3[added_in_v3["field"] == field]

        field_summary.append({
            "field": field,
            "v2_count": len(v2_field),
            "v3_count": len(v3_field),
            "exact_matches": len(match_field),
            "missing_from_v3": len(missing_field),
            "added_or_changed_in_v3": len(added_field),
        })

    field_summary_df = pd.DataFrame(field_summary)

    summary_df.to_csv(
        OUTPUT_DIR / "v2_v3_overlap_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    field_summary_df.to_csv(
        OUTPUT_DIR / "v2_v3_overlap_by_field.csv",
        index=False,
        encoding="utf-8-sig",
    )

    exact_matches.to_csv(
        OUTPUT_DIR / "v2_exact_matches_in_v3.csv",
        index=False,
        encoding="utf-8-sig",
    )

    missing_from_v3.to_csv(
        OUTPUT_DIR / "v2_occupations_missing_from_v3.csv",
        index=False,
        encoding="utf-8-sig",
    )

    added_in_v3.to_csv(
        OUTPUT_DIR / "v3_added_or_changed_occupations.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("v2-v3 occupation overlap audit completed.")
    print("Output:", OUTPUT_DIR)

    print("\nSummary:")
    print(summary_df.to_string(index=False))

    print("\nBy field:")
    print(field_summary_df.to_string(index=False))

    print("\nMissing v2 occupations from v3:")
    cols = ["field", "masculine_occupation", "feminine_occupation"]
    print(missing_from_v3[cols].to_string(index=False))


if __name__ == "__main__":
    main()