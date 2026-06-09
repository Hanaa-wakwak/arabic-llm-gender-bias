import argparse
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a quality report for Arabic gender minimal-pair scoring results."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to scoring results CSV file."
    )

    parser.add_argument(
        "--output_dir",
        default="results",
        help="Directory where quality report files will be saved."
    )

    parser.add_argument(
        "--prefix",
        required=True,
        help="Prefix for output files, e.g. v03."
    )

    parser.add_argument(
        "--outlier_threshold",
        type=float,
        default=0.75,
        help="Absolute score difference threshold for row-level outliers."
    )

    parser.add_argument(
        "--avg_threshold",
        type=float,
        default=0.30,
        help="Average score difference threshold for group-level warnings."
    )

    parser.add_argument(
        "--dominance_threshold",
        type=float,
        default=75.0,
        help="Preference percentage threshold for group-level dominance warnings."
    )

    return parser.parse_args()


def preferred_gender_percentages(group):
    total = len(group)
    masculine_count = int((group["preferred_gender"] == "masculine").sum())
    feminine_count = int((group["preferred_gender"] == "feminine").sum())
    equal_count = int((group["preferred_gender"] == "equal").sum())

    return {
        "total_items": total,
        "masculine_preferred_count": masculine_count,
        "feminine_preferred_count": feminine_count,
        "equal_count": equal_count,
        "masculine_preferred_percent": masculine_count / total * 100,
        "feminine_preferred_percent": feminine_count / total * 100,
        "equal_percent": equal_count / total * 100,
    }


def analyze_group(df, group_col, avg_threshold, dominance_threshold):
    rows = []

    for group_value, group in df.groupby(group_col):
        stats = preferred_gender_percentages(group)

        avg_diff = group["score_difference"].mean()
        median_diff = group["score_difference"].median()
        min_diff = group["score_difference"].min()
        max_diff = group["score_difference"].max()

        warnings = []

        if abs(avg_diff) >= avg_threshold:
            warnings.append("high_average_score_difference")

        if stats["masculine_preferred_percent"] >= dominance_threshold:
            warnings.append("masculine_preference_dominance")

        if stats["feminine_preferred_percent"] >= dominance_threshold:
            warnings.append("feminine_preference_dominance")

        if avg_diff > 0:
            average_direction = "masculine"
        elif avg_diff < 0:
            average_direction = "feminine"
        else:
            average_direction = "neutral"

        rows.append({
            group_col: group_value,
            "total_items": stats["total_items"],
            "average_score_difference": avg_diff,
            "average_direction": average_direction,
            "median_score_difference": median_diff,
            "min_score_difference": min_diff,
            "max_score_difference": max_diff,
            "masculine_preferred_count": stats["masculine_preferred_count"],
            "feminine_preferred_count": stats["feminine_preferred_count"],
            "equal_count": stats["equal_count"],
            "masculine_preferred_percent": stats["masculine_preferred_percent"],
            "feminine_preferred_percent": stats["feminine_preferred_percent"],
            "equal_percent": stats["equal_percent"],
            "warnings": ";".join(warnings) if warnings else "ok",
        })

    return pd.DataFrame(rows)


def main():
    args = parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "masculine_sentence",
        "feminine_sentence",
        "score_difference",
        "preferred_gender",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    print("=" * 80)
    print("Arabic Gender Bias Benchmark Quality Report")
    print("=" * 80)
    print(f"Input file: {input_path}")
    print(f"Rows: {len(df)}")
    print(f"Outlier threshold: {args.outlier_threshold}")
    print(f"Average threshold: {args.avg_threshold}")
    print(f"Dominance threshold: {args.dominance_threshold}%")

    # -------------------------------------------------
    # Row-level outliers
    # -------------------------------------------------
    df["absolute_score_difference"] = df["score_difference"].abs()

    outliers = df[df["absolute_score_difference"] >= args.outlier_threshold].copy()
    outliers = outliers.sort_values("absolute_score_difference", ascending=False)

    outlier_path = output_dir / f"quality_outliers_{args.prefix}.csv"
    outliers.to_csv(outlier_path, index=False, encoding="utf-8-sig")

    # -------------------------------------------------
    # Group-level reports
    # -------------------------------------------------
    group_cols = [
        "dialect",
        "dimension",
        "stereotype_direction",
        "template_id",
        "template_type",
        "concept_id",
    ]

    created_reports = []

    for col in group_cols:
        if col in df.columns:
            report = analyze_group(
                df=df,
                group_col=col,
                avg_threshold=args.avg_threshold,
                dominance_threshold=args.dominance_threshold,
            )

            report_path = output_dir / f"quality_by_{col}_{args.prefix}.csv"
            report.to_csv(report_path, index=False, encoding="utf-8-sig")
            created_reports.append(report_path)

            print(f"\nQuality by {col}:")
            print(report)

    # -------------------------------------------------
    # Overall decision helper
    # -------------------------------------------------
    total_items = len(df)
    total_outliers = len(outliers)
    outlier_percent = total_outliers / total_items * 100

    overall_avg = df["score_difference"].mean()
    overall_median = df["score_difference"].median()

    decision_notes = []

    if abs(overall_avg) < 0.10:
        decision_notes.append("overall_average_is_close_to_zero")
    else:
        decision_notes.append("overall_average_needs_review")

    if outlier_percent <= 25:
        decision_notes.append("outlier_rate_is_acceptable_for_pilot")
    else:
        decision_notes.append("outlier_rate_is_high")

    if "template_id" in df.columns:
        template_report = analyze_group(
            df=df,
            group_col="template_id",
            avg_threshold=args.avg_threshold,
            dominance_threshold=args.dominance_threshold,
        )

        problematic_templates = template_report[
            template_report["warnings"] != "ok"
        ]

        if len(problematic_templates) > 0:
            decision_notes.append("some_templates_need_revision")
        else:
            decision_notes.append("templates_are_stable")

    if "concept_id" in df.columns:
        concept_report = analyze_group(
            df=df,
            group_col="concept_id",
            avg_threshold=args.avg_threshold,
            dominance_threshold=args.dominance_threshold,
        )

        problematic_concepts = concept_report[
            concept_report["warnings"] != "ok"
        ]

        if len(problematic_concepts) > 0:
            decision_notes.append("some_concepts_need_review")
        else:
            decision_notes.append("concepts_are_stable")

    overall_report = pd.DataFrame([{
        "total_items": total_items,
        "total_outliers": total_outliers,
        "outlier_percent": outlier_percent,
        "overall_average_score_difference": overall_avg,
        "overall_median_score_difference": overall_median,
        "decision_notes": ";".join(decision_notes),
    }])

    overall_path = output_dir / f"quality_overall_{args.prefix}.csv"
    overall_report.to_csv(overall_path, index=False, encoding="utf-8-sig")

    print("\nOverall quality report:")
    print(overall_report)

    print("\nSaved files:")
    print(outlier_path)
    print(overall_path)
    for path in created_reports:
        print(path)

    print("\nDone.")


if __name__ == "__main__":
    main()