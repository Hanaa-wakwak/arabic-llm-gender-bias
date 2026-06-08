import math
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm


# -----------------------------
# Config
# -----------------------------
DATA_PATH = Path("data/benchmark_v0/template_test_v01.csv")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

OUTPUT_PATH = RESULTS_DIR / "template_test_results_v01.csv"# Small Arabic GPT-2 model for the first pilot experiment
MODEL_NAME = "aubmindlab/aragpt2-base"


# -----------------------------
# Device
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")


# -----------------------------
# Load model and tokenizer
# -----------------------------
print(f"Loading model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

model.to(device)
model.eval()


# -----------------------------
# Sentence scoring function
# -----------------------------
def sentence_log_probability(sentence: str) -> float:
    """
    Computes average token log probability for a sentence.
    Higher score = model finds the sentence more likely.
    """

    inputs = tokenizer(sentence, return_tensors="pt")

    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=input_ids,
        )

    # outputs.loss is average negative log likelihood
    loss = outputs.loss.item()

    # Convert loss to log probability score
    avg_log_prob = -loss

    return avg_log_prob


# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

print("\nDataset loaded:")
print(df.shape)


# -----------------------------
# Score pairs
# -----------------------------
results = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    masculine_sentence = row["masculine_sentence"]
    feminine_sentence = row["feminine_sentence"]

    masculine_score = sentence_log_probability(masculine_sentence)
    feminine_score = sentence_log_probability(feminine_sentence)

    score_difference = masculine_score - feminine_score

    if score_difference > 0:
        preferred_gender = "masculine"
    elif score_difference < 0:
        preferred_gender = "feminine"
    else:
        preferred_gender = "equal"

    results.append({
    "id": row["id"],
    "dialect": row["dialect"],
    "template_type": row["template_type"],
    "masculine_sentence": masculine_sentence,
    "feminine_sentence": feminine_sentence,
    "masculine_score": masculine_score,
    "feminine_score": feminine_score,
    "score_difference": score_difference,
    "preferred_gender": preferred_gender,
})


# -----------------------------
# Save results
# -----------------------------
results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print("\nScoring completed.")
print(f"Results saved to: {OUTPUT_PATH}")

print("\nFirst 10 results:")
print(results_df.head(10))

print("\nPreferred gender counts:")
print(results_df["preferred_gender"].value_counts())

print("\nAverage score difference by dialect:")
print(results_df.groupby("dialect")["score_difference"].mean())

print("\nAverage score difference by dimension:")
print(results_df.groupby("dimension")["score_difference"].mean())

print("\nAverage score difference by stereotype direction:")
print(results_df.groupby("stereotype_direction")["score_difference"].mean())