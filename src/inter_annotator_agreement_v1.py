from pathlib import Path
import argparse
from collections import Counter

import pandas as pd


def normalize_yes_no(value):
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    if value in ["yes", "y", "true", "1", "نعم", "اه", "أه"]:
        return "yes"

    if value in ["no", "n", "false", "0", "لا"]:
        return "no"

    return value


def normalize_decision(value):
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    if value in ["keep", "k", "احتفظ", "تمام"]:
        return "keep"

    if value in ["revise", "r", "edit", "تعديل"]:
        return "revise"

    if value in ["remove", "delete", "حذف"]:
        return "remove"

    return value


def fleiss_kappa(rating_matrix):
    """
    rating_matrix:
    rows = items
    columns = categories
    values = number of annotators who selected that category
    """
    n_items = len(rating_matrix)

    if n_items == 0:
        return None

    n_annotators = sum(rating_matrix[0])

    if n_annotators <= 1:
        return None

    p_i_values = []

    for row in rating_matrix:
        row_sum = sum(row)

        if row_sum != n_annotators:
            raise ValueError("All rows must have the same number of annotators.")

        p_i = (sum(count * count for count in row) - n_annotators) / (
            n_annotators * (n_annotators - 1)
        )
        p_i_values.append(p_i)

    p_bar = sum(p_i_values) / n_items

    category_totals = [sum(row[j] for row in rating_matrix) for j in range(len(rating_matrix[0]))]
    total_ratings = n_items * n_annotators

    p_j_values = [category_total / total_ratings for category_total in category_totals]
    p_e_bar = sum(p_j * p_j for p_j in p_j_values)

    if p_e_bar == 1:
        return 1.0

    kappa = (p_bar - p_e_bar) / (1 - p_e_bar)

    return kappa


def build_rating_matrix(merged_df, annotator_columns, categories):
    matrix = []

    for _, row in merged_df.iterrows():
        ratings = [row[col] for col in annotator_columns]
        counts = Counter(ratings)
        matrix.append([counts.get(category, 0) for category in categories])

    return matrix


def interpret_kappa(kappa):
    if kappa is None:
        return "not_available"

    if kappa < 0:
        return "poor"
    if kappa < 0.20:
        return "slight"
    if kappa < 0.40:
        return "fair"
    if kappa < 0.60:
        return "moderate"
    if kappa < 0.80:
        return "substantial"

    return "almost_perfect"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--annotator_files",
        required=True,
        nargs="+",
        help="List of filled human validation CSV files, one per annotator.",
    )

    parser.add_argument(
        "--output_dir",
        default="results/occupational_benchmark_v1/human_validation_agreement",
        help="Output directory.",
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    annotator_dfs = []

    for index, file_path in enumerate(args.annotator_files, start=1):
        path = Path(file_path)
        df = pd.read_csv(path, encoding="utf-8-sig")

        required_columns = [
            "id",
            "dialect_correct_yes_no",
            "gender_pair_correct_yes_no",
            "occupation_field_correct_yes_no",
            "final_decision_keep_revise_remove",
        ]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            raise ValueError(f"{path} is missing columns: {missing}")

        annotator_label = f"annotator_{index}"

        small_df = df[required_columns].copy()
        small_df[f"dialect_correct_{annotator_label}"] = small_df["dialect_correct_yes_no"].apply(normalize_yes_no)
        small_df[f"gender_pair_correct_{annotator_label}"] = small_df["gender_pair_correct_yes_no"].apply(normalize_yes_no)
        small_df[f"occupation_field_correct_{annotator_label}"] = small_df["occupation_field_correct_yes_no"].apply(normalize_yes_no)
        small_df[f"final_decision_{annotator_label}"] = small_df["final_decision_keep_revise_remove"].apply(normalize_decision)

        keep_cols = [
            "id",
            f"dialect_correct_{annotator_label}",
            f"gender_pair_correct_{annotator_label}",
            f"occupation_field_correct_{annotator_label}",
            f"final_decision_{annotator_label}",
        ]

        annotator_dfs.append(small_df[keep_cols])

    merged = annotator_dfs[0]

    for next_df in annotator_dfs[1:]:
        merged = merged.merge(next_df, on="id", how="inner")

    merged.to_csv(
        output_dir / "merged_annotator_ratings.csv",
        index=False,
        encoding="utf-8-sig",
    )

    checks = {
        "dialect_correct": ["yes", "no"],
        "gender_pair_correct": ["yes", "no"],
        "occupation_field_correct": ["yes", "no"],
        "final_decision": ["keep", "revise", "remove"],
    }

    rows = []

    for check_name, categories in checks.items():
        annotator_columns = [
            col for col in merged.columns
            if col.startswith(f"{check_name}_annotator_")
        ]

        matrix = build_rating_matrix(
            merged,
            annotator_columns,
            categories,
        )

        kappa = fleiss_kappa(matrix)

        rows.append({
            "criterion": check_name,
            "num_items": len(merged),
            "num_annotators": len(annotator_columns),
            "categories": "|".join(categories),
            "fleiss_kappa": kappa,
            "interpretation": interpret_kappa(kappa),
        })

    agreement_df = pd.DataFrame(rows)

    agreement_df.to_csv(
        output_dir / "inter_annotator_agreement_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Inter-annotator agreement completed.")
    print("Outputs saved to:")
    print(output_dir)
    print(agreement_df)


if __name__ == "__main__":
    main()