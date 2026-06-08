import argparse
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(
        description="Score Arabic gender minimal pairs using a causal language model."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV file containing masculine_sentence and feminine_sentence columns.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to output CSV file.",
    )

    parser.add_argument(
        "--model",
        default="aubmindlab/aragpt2-base",
        help="HuggingFace model name.",
    )

    return parser.parse_args()


def sentence_log_probability(sentence, tokenizer, model, device):
    inputs = tokenizer(sentence, return_tensors="pt")

    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=input_ids,
        )

    loss = outputs.loss.item()
    return -loss


def main():
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("=" * 70)
    print("Arabic Gender Minimal Pair Scoring")
    print("=" * 70)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Model: {args.model}")
    print(f"Device: {device}")

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = ["masculine_sentence", "feminine_sentence"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model)

    model.to(device)
    model.eval()

    results = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        masculine_sentence = row["masculine_sentence"]
        feminine_sentence = row["feminine_sentence"]

        masculine_score = sentence_log_probability(
            masculine_sentence, tokenizer, model, device
        )

        feminine_score = sentence_log_probability(
            feminine_sentence, tokenizer, model, device
        )

        score_difference = masculine_score - feminine_score

        if score_difference > 0:
            preferred_gender = "masculine"
        elif score_difference < 0:
            preferred_gender = "feminine"
        else:
            preferred_gender = "equal"

        result_row = row.to_dict()
        result_row["masculine_score"] = masculine_score
        result_row["feminine_score"] = feminine_score
        result_row["score_difference"] = score_difference
        result_row["preferred_gender"] = preferred_gender

        results.append(result_row)

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("\nScoring completed.")
    print(f"Saved to: {output_path}")

    print("\nPreferred gender counts:")
    print(results_df["preferred_gender"].value_counts())

    print("\nAverage score difference:")
    print(results_df["score_difference"].mean())

    print("\nMedian score difference:")
    print(results_df["score_difference"].median())


if __name__ == "__main__":
    main()