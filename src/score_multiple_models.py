from pathlib import Path
import argparse
import gc

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm


DEFAULT_MODELS = [
    "aubmindlab/aragpt2-base",
    "aubmindlab/aragpt2-medium",
    "bigscience/bloom-560m",
    "bigscience/bloom-1b1",
]


def safe_model_name(model_name: str) -> str:
    return model_name.replace("/", "__").replace("-", "_")


def load_model_and_tokenizer(model_name: str, device: str):
    print("=" * 80)
    print(f"Loading model: {model_name}")
    print("=" * 80)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model.to(device)
    model.eval()

    return tokenizer, model


def sentence_log_probability(sentence: str, tokenizer, model, device: str) -> float:
    inputs = tokenizer(
        sentence,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=input_ids,
        )

    loss = outputs.loss.item()
    avg_log_prob = -loss

    return avg_log_prob


def score_model(model_name: str, df: pd.DataFrame, output_dir: Path, device: str):
    tokenizer, model = load_model_and_tokenizer(model_name, device)

    scored_rows = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Scoring {model_name}"):
        masculine_sentence = row["masculine_sentence"]
        feminine_sentence = row["feminine_sentence"]

        masculine_score = sentence_log_probability(
            masculine_sentence,
            tokenizer,
            model,
            device,
        )

        feminine_score = sentence_log_probability(
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

        scored_row = row.to_dict()
        scored_row["model_name"] = model_name
        scored_row["masculine_score"] = masculine_score
        scored_row["feminine_score"] = feminine_score
        scored_row["score_difference"] = score_difference
        scored_row["preferred_gender"] = preferred_gender

        scored_rows.append(scored_row)

    result_df = pd.DataFrame(scored_rows)

    model_file_name = safe_model_name(model_name)
    output_path = output_dir / f"scoring_results_v07_{model_file_name}.csv"
    result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\nSaved model results to: {output_path}")

    del model
    del tokenizer
    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return result_df


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        default="data/benchmark_v0/minimal_pairs_v07.csv",
        help="Input benchmark CSV file.",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default="results/model_comparison_v07",
        help="Output directory for model comparison results.",
    )

    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_MODELS,
        help="List of Hugging Face causal language models.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("Device:")
    print(device)

    print("\nInput benchmark:")
    print(input_path)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required_columns = [
        "masculine_sentence",
        "feminine_sentence",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    all_results = []

    for model_name in args.models:
        model_results = score_model(
            model_name=model_name,
            df=df,
            output_dir=output_dir,
            device=device,
        )

        all_results.append(model_results)

    combined_df = pd.concat(all_results, ignore_index=True)

    combined_output_path = output_dir / "scoring_results_v07_all_models.csv"
    combined_df.to_csv(combined_output_path, index=False, encoding="utf-8-sig")

    print("\nCombined results saved to:")
    print(combined_output_path)


if __name__ == "__main__":
    main()