from pathlib import Path
import argparse
import inspect

import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fine-tune a causal LM on balanced Arabic masculine-feminine counterfactual data."
    )

    parser.add_argument(
        "--model_name",
        default="aubmindlab/aragpt2-base",
        help="Base causal LM name from Hugging Face or local model path.",
    )

    parser.add_argument(
        "--train_file",
        default="data/q1_bias_mitigation/arabic_counterfactual_mitigation_train.txt",
        help="Plain text training file. One sentence per line.",
    )

    parser.add_argument(
        "--output_dir",
        default="models/q1_mitigation/aragpt2_base_counterfactual_cda",
        help="Output directory for the mitigated model.",
    )

    parser.add_argument("--max_length", type=int, default=128)
    parser.add_argument("--num_train_epochs", type=float, default=1.0)
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument("--batch_size", type=int, default=2)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=8)
    parser.add_argument("--save_steps", type=int, default=500)
    parser.add_argument("--logging_steps", type=int, default=50)

    return parser.parse_args()


def load_lines(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Training file not found: {path}")

    text = path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        raise ValueError(f"Training file is empty: {path}")

    return lines


def tokenize_dataset(dataset, tokenizer, max_length):
    def tokenize(batch):
        tokenized = tokenizer(
            batch["text"],
            truncation=True,
            max_length=max_length,
            padding="max_length",
        )

        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized

    return dataset.map(tokenize, batched=True, remove_columns=["text"])


def build_training_args(args, output_dir, device_has_cuda):
    training_kwargs = {
        "output_dir": str(output_dir),
        "overwrite_output_dir": True,
        "num_train_epochs": args.num_train_epochs,
        "per_device_train_batch_size": args.batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "learning_rate": args.learning_rate,
        "logging_steps": args.logging_steps,
        "save_steps": args.save_steps,
        "save_total_limit": 2,
        "fp16": device_has_cuda,
        "report_to": [],
        "remove_unused_columns": False,
    }

    supported_args = set(inspect.signature(TrainingArguments.__init__).parameters)

    filtered_kwargs = {
        key: value
        for key, value in training_kwargs.items()
        if key in supported_args
    }

    return TrainingArguments(**filtered_kwargs)


def build_trainer(model, training_args, tokenized, tokenizer, data_collator):
    trainer_kwargs = {
        "model": model,
        "args": training_args,
        "train_dataset": tokenized,
        "tokenizer": tokenizer,
        "data_collator": data_collator,
    }

    supported_trainer_args = set(inspect.signature(Trainer.__init__).parameters)

    filtered_kwargs = {
        key: value
        for key, value in trainer_kwargs.items()
        if key in supported_trainer_args
    }

    return Trainer(**filtered_kwargs)


def main():
    args = parse_args()

    train_path = Path(args.train_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    lines = load_lines(train_path)

    dataset = Dataset.from_dict({"text": lines})

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    tokenized = tokenize_dataset(dataset, tokenizer, args.max_length)

    device_has_cuda = torch.cuda.is_available()

    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=torch.float16 if device_has_cuda else torch.float32,
    )

    if tokenizer.pad_token_id is not None:
        model.config.pad_token_id = tokenizer.pad_token_id

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    training_args = build_training_args(args, output_dir, device_has_cuda)

    trainer = build_trainer(
        model=model,
        training_args=training_args,
        tokenized=tokenized,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()

    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    readme = output_dir / "README_MITIGATION_MODEL.md"
    readme.write_text(
        "\n".join(
            [
                "# Q1 Counterfactual Mitigation Model",
                "",
                f"Base model: `{args.model_name}`",
                "",
                f"Training file: `{args.train_file}`",
                "",
                "This model was fine-tuned on balanced Arabic masculine-feminine occupational counterfactual sentences.",
                "",
                "Purpose:",
                "",
                "- Test whether counterfactual data augmentation reduces occupational gender preference.",
                "- Compare benchmark scores before and after mitigation.",
                "",
                "Main mitigation evaluation:",
                "",
                "Mitigation_Gain = |Bias_before| - |Bias_after|",
                "",
                "This model is an experimental research artifact, not a production-safe debiased model.",
            ]
        ),
        encoding="utf-8",
    )

    print("Fine-tuning complete.")
    print("Base model:", args.model_name)
    print("Training file:", train_path)
    print("Training sentences:", len(lines))
    print("Mitigated model saved to:", output_dir)


if __name__ == "__main__":
    main()