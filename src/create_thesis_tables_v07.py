from pathlib import Path
import pandas as pd


INPUT_DIR = Path("results/model_comparison_v07")
OUTPUT_DIR = Path("results/thesis_tables_v07")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_model_name(name):
    return (
        name.replace("aubmindlab/", "")
        .replace("bigscience/", "")
    )


def save_table(df, name):
    csv_path = OUTPUT_DIR / f"{name}.csv"
    md_path = OUTPUT_DIR / f"{name}.md"

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(df.to_markdown(index=False))

    print(f"Saved: {csv_path}")
    print(f"Saved: {md_path}")


def create_overall_table():
    df = pd.read_csv(INPUT_DIR / "model_comparison_overall_summary.csv", encoding="utf-8-sig")

    table = pd.DataFrame({
        "Model": df["model_name"].apply(clean_model_name),
        "Masculine Preferred": df["masculine_preferred_count"],
        "Feminine Preferred": df["feminine_preferred_count"],
        "Masculine %": df["masculine_preferred_percent"].round(2),
        "Feminine %": df["feminine_preferred_percent"].round(2),
        "Avg Score Diff": df["average_score_difference"].round(4),
        "Median Score Diff": df["median_score_difference"].round(4),
    })

    save_table(table, "table_overall_model_comparison")


def create_dialect_table():
    df = pd.read_csv(INPUT_DIR / "model_comparison_by_dialect.csv", encoding="utf-8-sig")
    df["Model"] = df["model_name"].apply(clean_model_name)

    table = df[
        [
            "Model",
            "dialect",
            "masculine_preferred_count",
            "feminine_preferred_count",
            "masculine_preferred_percent",
            "feminine_preferred_percent",
            "average_score_difference",
        ]
    ].copy()

    table.columns = [
        "Model",
        "Dialect",
        "Masculine Preferred",
        "Feminine Preferred",
        "Masculine %",
        "Feminine %",
        "Avg Score Diff",
    ]

    table["Masculine %"] = table["Masculine %"].round(2)
    table["Feminine %"] = table["Feminine %"].round(2)
    table["Avg Score Diff"] = table["Avg Score Diff"].round(4)

    save_table(table, "table_dialect_model_comparison")


def create_dimension_table():
    df = pd.read_csv(INPUT_DIR / "model_comparison_by_dimension.csv", encoding="utf-8-sig")
    df["Model"] = df["model_name"].apply(clean_model_name)

    table = df[
        [
            "Model",
            "dimension",
            "masculine_preferred_count",
            "feminine_preferred_count",
            "masculine_preferred_percent",
            "feminine_preferred_percent",
            "average_score_difference",
        ]
    ].copy()

    table.columns = [
        "Model",
        "Dimension",
        "Masculine Preferred",
        "Feminine Preferred",
        "Masculine %",
        "Feminine %",
        "Avg Score Diff",
    ]

    table["Masculine %"] = table["Masculine %"].round(2)
    table["Feminine %"] = table["Feminine %"].round(2)
    table["Avg Score Diff"] = table["Avg Score Diff"].round(4)

    save_table(table, "table_dimension_model_comparison")


def create_stereotype_table():
    df = pd.read_csv(INPUT_DIR / "model_comparison_by_stereotype_direction.csv", encoding="utf-8-sig")
    df["Model"] = df["model_name"].apply(clean_model_name)

    table = df[
        [
            "Model",
            "stereotype_direction",
            "masculine_preferred_count",
            "feminine_preferred_count",
            "masculine_preferred_percent",
            "feminine_preferred_percent",
            "average_score_difference",
        ]
    ].copy()

    table.columns = [
        "Model",
        "Stereotype Direction",
        "Masculine Preferred",
        "Feminine Preferred",
        "Masculine %",
        "Feminine %",
        "Avg Score Diff",
    ]

    table["Masculine %"] = table["Masculine %"].round(2)
    table["Feminine %"] = table["Feminine %"].round(2)
    table["Avg Score Diff"] = table["Avg Score Diff"].round(4)

    save_table(table, "table_stereotype_model_comparison")


def main():
    create_overall_table()
    create_dialect_table()
    create_dimension_table()
    create_stereotype_table()

    print("\nAll thesis-ready tables saved to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()