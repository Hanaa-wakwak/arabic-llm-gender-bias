from pathlib import Path
import pandas as pd


INPUT_PATH = Path("results/statistical_tests_v07/pairwise_model_wilcoxon_tests.csv")
OUTPUT_PATH = Path("results/statistical_tests_v07/pairwise_model_wilcoxon_tests_corrected.csv")


def bonferroni_correction(p_values):
    m = len(p_values)
    return [min(p * m, 1.0) for p in p_values]


def holm_correction(p_values):
    """
    Holm-Bonferroni adjusted p-values.
    """
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])

    adjusted = [None] * m
    running_max = 0

    for rank, (original_idx, p) in enumerate(indexed):
        corrected = (m - rank) * p
        corrected = min(corrected, 1.0)

        running_max = max(running_max, corrected)
        adjusted[original_idx] = min(running_max, 1.0)

    return adjusted


def benjamini_hochberg_correction(p_values):
    """
    Benjamini-Hochberg FDR adjusted p-values.
    """
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1], reverse=True)

    adjusted = [None] * m
    running_min = 1.0

    for rank_from_largest, (original_idx, p) in enumerate(indexed):
        rank = m - rank_from_largest
        corrected = (p * m) / rank
        corrected = min(corrected, 1.0)

        running_min = min(running_min, corrected)
        adjusted[original_idx] = running_min

    return adjusted


def main():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    if "wilcoxon_p_value" not in df.columns:
        raise ValueError("Missing column: wilcoxon_p_value")

    p_values = df["wilcoxon_p_value"].tolist()

    df["p_bonferroni"] = bonferroni_correction(p_values)
    df["p_holm"] = holm_correction(p_values)
    df["p_bh_fdr"] = benjamini_hochberg_correction(p_values)

    df["significant_bonferroni_0_05"] = df["p_bonferroni"] < 0.05
    df["significant_holm_0_05"] = df["p_holm"] < 0.05
    df["significant_bh_fdr_0_05"] = df["p_bh_fdr"] < 0.05

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Corrected pairwise tests saved to:")
    print(OUTPUT_PATH)

    print("\nCorrected summary:")
    print(
        df[
            [
                "model_a",
                "model_b",
                "wilcoxon_p_value",
                "p_bonferroni",
                "p_holm",
                "p_bh_fdr",
                "significant_bonferroni_0_05",
                "significant_holm_0_05",
                "significant_bh_fdr_0_05",
            ]
        ]
    )


if __name__ == "__main__":
    main()