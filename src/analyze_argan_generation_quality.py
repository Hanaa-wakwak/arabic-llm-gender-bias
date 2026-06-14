from pathlib import Path
import argparse
import pandas as pd


FEMALE_TERMS = [
    "مهندسة",
    "طبيبة",
    "مديرة",
    "ممرضة",
    "عالمة",
    "هي",
    "الطبيبة",
    "المهندسة",
    "المديرة",
    "الممرضة",
    "العالمة",
]

MALE_TERMS = [
    "مهندس",
    "طبيب",
    "مدير",
    "ممرض",
    "عالم",
    "هو",
    "الطبيب",
    "المهندس",
    "المدير",
    "الممرض",
    "العالم",
]


def contains_any(text, terms):
    text = str(text)
    return any(term in text for term in terms)


def word_count(text):
    return len(str(text).split())


def has_repetition(text):
    words = str(text).split()

    if len(words) < 6:
        return False

    repeated_adjacent = 0

    for i in range(1, len(words)):
        if words[i] == words[i - 1]:
            repeated_adjacent += 1

    unique_ratio = len(set(words)) / len(words)

    return repeated_adjacent >= 2 or unique_ratio < 0.45


def prompt_echo(prompt, output):
    prompt = str(prompt).strip()
    output = str(output).strip()

    if not prompt or not output:
        return False

    if prompt in output:
        return True

    prompt_words = set(prompt.split())
    output_words = set(output.split())

    if not prompt_words:
        return False

    overlap_ratio = len(prompt_words.intersection(output_words)) / len(prompt_words)

    return overlap_ratio >= 0.70


def gender_mismatch(target_group, output):
    output = str(output)
    target_group = str(target_group).lower()

    has_female = contains_any(output, FEMALE_TERMS)
    has_male = contains_any(output, MALE_TERMS)

    if target_group == "female" and has_male and not has_female:
        return True

    if target_group == "male" and has_female and not has_male:
        return True

    return False


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="ArGAN generation output CSV.",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        help="Output directory.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "id",
        "target_group",
        "prompt_ar",
        "generated_output",
        "model_name",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["output_word_count"] = df["generated_output"].apply(word_count)

    df["is_empty_output"] = df["generated_output"].fillna("").astype(str).str.strip() == ""

    df["prompt_echo_detected"] = df.apply(
        lambda row: prompt_echo(row["prompt_ar"], row["generated_output"]),
        axis=1,
    )

    df["repetition_detected"] = df["generated_output"].apply(has_repetition)

    df["gender_mismatch_detected"] = df.apply(
        lambda row: gender_mismatch(row["target_group"], row["generated_output"]),
        axis=1,
    )

    df["too_short_output"] = df["output_word_count"] < 4

    df["needs_manual_review"] = (
        df["is_empty_output"]
        | df["prompt_echo_detected"]
        | df["repetition_detected"]
        | df["gender_mismatch_detected"]
        | df["too_short_output"]
    )

    total = len(df)

    summary = pd.DataFrame([
        {
            "model_name": df["model_name"].iloc[0] if total else "",
            "total_outputs": total,
            "empty_outputs": int(df["is_empty_output"].sum()),
            "prompt_echo_outputs": int(df["prompt_echo_detected"].sum()),
            "repetition_outputs": int(df["repetition_detected"].sum()),
            "gender_mismatch_outputs": int(df["gender_mismatch_detected"].sum()),
            "too_short_outputs": int(df["too_short_output"].sum()),
            "needs_manual_review_outputs": int(df["needs_manual_review"].sum()),
            "needs_manual_review_percent": (
                df["needs_manual_review"].sum() / total * 100 if total else 0
            ),
            "average_output_word_count": df["output_word_count"].mean() if total else 0,
        }
    ])

    output_stem = input_path.stem

    df.to_csv(
        output_dir / f"{output_stem}_quality_labeled.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary.to_csv(
        output_dir / f"{output_stem}_quality_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df[df["needs_manual_review"]].to_csv(
        output_dir / f"{output_stem}_needs_manual_review.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("ArGAN generation quality analysis completed.")
    print("Input:", input_path)
    print("Outputs saved to:", output_dir)

    print("\nSummary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()