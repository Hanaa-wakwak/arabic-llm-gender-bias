from pathlib import Path
import argparse

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


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
        help="Hugging Face causal language model name.",
    )

    parser.add_argument(
        "--input",
        default="data/external_datasets/argan/argan_gender_pilot_sample.csv",
        help="ArGAN-format prompt CSV file.",
    )

    parser.add_argument(
        "--output_dir",
        default="results/external_datasets/argan",
        help="Directory to save generated outputs.",
    )

    parser.add_argument(
        "--prompt_col",
        default="prompt_ar",
        help="Column containing Arabic prompts.",
    )

    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=40,
        help="Maximum number of generated tokens.",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature.",
    )

    parser.add_argument(
        "--top_p",
        type=float,
        default=0.9,
        help="Top-p nucleus sampling value.",
    )

    parser.add_argument(
        "--do_sample",
        action="store_true",
        help="Use sampling instead of deterministic generation.",
    )

    parser.add_argument(
        "--trust_remote_code",
        action="store_true",
        help="Allow loading models that require custom Hugging Face code.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_slug = safe_model_slug(args.model_name)
    output_path = output_dir / f"argan_generation_results_{model_slug}.csv"

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    if args.prompt_col not in df.columns:
        raise ValueError(
            f"Prompt column not found: {args.prompt_col}. "
            f"Available columns: {list(df.columns)}"
        )

    print(f"Loading model: {args.model_name}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name,
        trust_remote_code=args.trust_remote_code,
    )

    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        trust_remote_code=args.trust_remote_code,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model.to(device)
    model.eval()

    generated_outputs = []

    for idx, row in df.iterrows():
        prompt = str(row[args.prompt_col]).strip()

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(device)

        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=args.do_sample,
                temperature=args.temperature if args.do_sample else None,
                top_p=args.top_p if args.do_sample else None,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        input_length = inputs["input_ids"].shape[-1]
        new_tokens = generated_ids[0][input_length:]

        generated_text = tokenizer.decode(
            new_tokens,
            skip_special_tokens=True,
        ).strip()

        generated_outputs.append(generated_text)

        print(f"Processed {idx + 1}/{len(df)} prompts")

    df["model_name"] = args.model_name
    df["generated_output"] = generated_outputs
    df["generation_max_new_tokens"] = args.max_new_tokens
    df["generation_do_sample"] = args.do_sample
    df["generation_temperature"] = args.temperature
    df["generation_top_p"] = args.top_p

    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("\nArGAN generation completed.")
    print("Output saved to:")
    print(output_path)


if __name__ == "__main__":
    main()