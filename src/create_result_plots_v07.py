from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


INPUT_DIR = Path("results/model_comparison_v07")
OUTPUT_DIR = Path("results/figures_v07")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_model_name(name):
    return (
        name.replace("aubmindlab/", "")
        .replace("bigscience/", "")
    )


def save_plot(path):
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


def plot_overall_preference_counts():
    df = pd.read_csv(INPUT_DIR / "model_comparison_overall_summary.csv", encoding="utf-8-sig")
    df["model_short"] = df["model_name"].apply(clean_model_name)

    x = range(len(df))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([i - width / 2 for i in x], df["masculine_preferred_count"], width, label="Masculine preferred")
    plt.bar([i + width / 2 for i in x], df["feminine_preferred_count"], width, label="Feminine preferred")

    plt.xticks(list(x), df["model_short"], rotation=20, ha="right")
    plt.ylabel("Number of items")
    plt.title("Overall Gender Preference Counts by Model")
    plt.legend()

    save_plot(OUTPUT_DIR / "overall_preference_counts_by_model.png")


def plot_overall_average_score_difference():
    df = pd.read_csv(INPUT_DIR / "model_comparison_overall_summary.csv", encoding="utf-8-sig")
    df["model_short"] = df["model_name"].apply(clean_model_name)

    plt.figure(figsize=(10, 6))
    plt.bar(df["model_short"], df["average_score_difference"])
    plt.axhline(0, linestyle="--", linewidth=1)

    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Average score difference")
    plt.title("Average Gender Score Difference by Model")

    save_plot(OUTPUT_DIR / "overall_average_score_difference_by_model.png")


def plot_dialect_average_score_difference():
    df = pd.read_csv(INPUT_DIR / "model_comparison_by_dialect.csv", encoding="utf-8-sig")
    df["model_short"] = df["model_name"].apply(clean_model_name)

    pivot = df.pivot(index="model_short", columns="dialect", values="average_score_difference")

    ax = pivot.plot(kind="bar", figsize=(10, 6))
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_ylabel("Average score difference")
    ax.set_title("Average Score Difference by Model and Dialect")
    ax.set_xlabel("Model")
    plt.xticks(rotation=20, ha="right")

    save_plot(OUTPUT_DIR / "dialect_average_score_difference_by_model.png")


def plot_dimension_preference_counts():
    df = pd.read_csv(INPUT_DIR / "model_comparison_by_dimension.csv", encoding="utf-8-sig")
    df["model_short"] = df["model_name"].apply(clean_model_name)

    for dimension in sorted(df["dimension"].unique()):
        sub = df[df["dimension"] == dimension].copy()

        x = range(len(sub))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar([i - width / 2 for i in x], sub["masculine_preferred_count"], width, label="Masculine preferred")
        plt.bar([i + width / 2 for i in x], sub["feminine_preferred_count"], width, label="Feminine preferred")

        plt.xticks(list(x), sub["model_short"], rotation=20, ha="right")
        plt.ylabel("Number of items")
        plt.title(f"Gender Preference Counts by Model — {dimension}")
        plt.legend()

        save_plot(OUTPUT_DIR / f"dimension_{dimension}_preference_counts_by_model.png")


def plot_stereotype_average_score_difference():
    df = pd.read_csv(INPUT_DIR / "model_comparison_by_stereotype_direction.csv", encoding="utf-8-sig")
    df["model_short"] = df["model_name"].apply(clean_model_name)

    pivot = df.pivot(
        index="model_short",
        columns="stereotype_direction",
        values="average_score_difference",
    )

    ax = pivot.plot(kind="bar", figsize=(11, 6))
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_ylabel("Average score difference")
    ax.set_title("Average Score Difference by Model and Stereotype Direction")
    ax.set_xlabel("Model")
    plt.xticks(rotation=20, ha="right")

    save_plot(OUTPUT_DIR / "stereotype_average_score_difference_by_model.png")


def main():
    plot_overall_preference_counts()
    plot_overall_average_score_difference()
    plot_dialect_average_score_difference()
    plot_dimension_preference_counts()
    plot_stereotype_average_score_difference()

    print("\nAll figures saved to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()