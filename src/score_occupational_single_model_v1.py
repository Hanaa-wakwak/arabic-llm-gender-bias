from pathlib import Path
import argparse

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def sentence_score(sentence, tokenizer, model, device):
    inputs = tokenizer(sentence, return_tensors="pt")
    input_ids = inputs["input_ids"].to(device)

    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        logits = outputs.logits

    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = input_ids[:, 1:].contiguous()

    log_probs = torch.nn.functional.log_softmax(shift_logits, dim=-1)
    token_log_probs = log_probs.gather(
        dim=-1,
        index=shift_labels.unsqueeze(-1),
    ).squeeze(-1)

    return token_log_probs.mean().item()


def safe_model_slug(model_name):
    return (
        model_name
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_name",
        required=True,
        help="HuggingFace model name.",
    )

    parser.add_argument(
        "--input",
        default="data/occupational_benchmark/occupational_bias_v1.csv",
        help="Input occupational benchmark CSV.",
    )

    parser.add_argument(
        "--output_dir",
        default="results/occupational_benchmark_v1",
        help="Output directory.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_name = args.model_name
    model_slug = safe_model_slug(model_name)

    output_path = output_dir / f"scoring_results_occupational_v1_{model_slug}.csv"

    print(f"Loading model: {model_name}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.to(device)
    model.eval()

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "masculine_sentence",
        "feminine_sentence",
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    masculine_scores = []
    feminine_scores = []
    score_differences = []
    preferred_genders = []

    for idx, row in df.iterrows():
        masculine_sentence = row["masculine_sentence"]
        feminine_sentence = row["feminine_sentence"]

        masculine_score = sentence_score(
            masculine_sentence,
            tokenizer,
            model,
            device,
        )

        feminine_score = sentence_score(
            feminine_sentence,
            tokenizer,
            model,
            device,
        )

        score_difference = masculine_score - feminine_score

        if score_difference > 0:
            preferred_gender = "masculine"
        elif score_difference < 0:
            preferred_gender = "feminine"
        else:
            preferred_gender = "equal"

        masculine_scores.append(masculine_score)
        feminine_scores.append(feminine_score)
        score_differences.append(score_difference)
        preferred_genders.append(preferred_gender)

        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{len(df)} pairs")

    df["model_name"] = model_name
    df["masculine_score"] = masculine_scores
    df["feminine_score"] = feminine_scores
    df["score_difference"] = score_differences
    df["preferred_gender"] = preferred_genders

    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    masculine_count = int((df["preferred_gender"] == "masculine").sum())
    feminine_count = int((df["preferred_gender"] == "feminine").sum())
    equal_count = int((df["preferred_gender"] == "equal").sum())

    print("\nScoring completed.")
    print(f"Output saved to: {output_path}")
    print(f"Total items: {len(df)}")
    print(f"Masculine preferred: {masculine_count}")
    print(f"Feminine preferred: {feminine_count}")
    print(f"Equal: {equal_count}")
    print(f"Average score_difference: {df['score_difference'].mean()}")


if __name__ == "__main__":
    main()