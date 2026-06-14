from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="ArGAN generation CSV file.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output annotation CSV file.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "id",
        "bias_axis",
        "target_group",
        "prompt_ar",
        "prompt_type",
        "expected_output_type",
        "model_name",
        "generated_output",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    annotation_df = df.copy()

    annotation_df["output_is_valid_yes_no"] = ""
    annotation_df["prompt_echo_yes_no"] = ""
    annotation_df["repetition_yes_no"] = ""
    annotation_df["stereotype_present_yes_no"] = ""
    annotation_df["gender_bias_direction"] = ""
    annotation_df["professional_neutrality_1_to_5"] = ""
    annotation_df["arabic_fluency_1_to_5"] = ""
    annotation_df["annotation_decision_keep_review_remove"] = ""
    annotation_df["annotator_comments"] = ""

    annotation_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("ArGAN annotation sheet created.")
    print("Input:", input_path)
    print("Output:", output_path)
    print("Rows:", len(annotation_df))


if __name__ == "__main__":
    main()