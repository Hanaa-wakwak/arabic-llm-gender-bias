from pathlib import Path
import pandas as pd


BENCHMARK_PATH = Path("data/benchmark_v0/minimal_pairs_v04.csv")
REVIEW_PATH = Path("data/review/manual_review_sheet_v04_completed.csv")
OUTPUT_PATH = Path("data/benchmark_v0/minimal_pairs_v05.csv")


def is_blank(value):
    return pd.isna(value) or str(value).strip() == ""


def main():
    benchmark_df = pd.read_csv(BENCHMARK_PATH, encoding="utf-8-sig")
    review_df = pd.read_csv(REVIEW_PATH, encoding="utf-8-sig")

    review_by_id = {
        int(row["id"]): row
        for _, row in review_df.iterrows()
    }

    output_rows = []

    rewritten_count = 0
    removed_count = 0
    kept_count = 0

    for _, row in benchmark_df.iterrows():
        item_id = int(row["id"])

        if item_id in review_by_id:
            review = review_by_id[item_id]

            keep_or_remove = str(review.get("keep_or_remove", "")).strip()
            manual_decision = str(review.get("manual_decision", "")).strip()

            if keep_or_remove == "remove":
                removed_count += 1
                continue

            new_row = row.copy()

            if manual_decision == "rewrite" or keep_or_remove == "keep_after_rewrite":
                revised_m = review.get("revised_masculine_sentence", "")
                revised_f = review.get("revised_feminine_sentence", "")

                if not is_blank(revised_m) and not is_blank(revised_f):
                    new_row["masculine_sentence"] = revised_m
                    new_row["feminine_sentence"] = revised_f
                    new_row["notes"] = str(new_row["notes"]) + " | rewritten_from_review"
                    rewritten_count += 1
                else:
                    kept_count += 1
            else:
                kept_count += 1

            output_rows.append(new_row)

        else:
            output_rows.append(row)
            kept_count += 1

    output_df = pd.DataFrame(output_rows)

    # Reassign IDs cleanly
    output_df = output_df.reset_index(drop=True)
    output_df["id"] = range(1, len(output_df) + 1)

    output_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Benchmark v0.5 saved to:")
    print(OUTPUT_PATH)

    print("\nShape:")
    print(output_df.shape)

    print("\nRewritten rows:")
    print(rewritten_count)

    print("\nRemoved rows:")
    print(removed_count)

    print("\nKept rows:")
    print(kept_count)

    print("\nCount by dialect:")
    print(output_df["dialect"].value_counts())

    print("\nCount by dimension:")
    print(output_df["dimension"].value_counts())

    print("\nCount by template_id:")
    print(output_df["template_id"].value_counts())


if __name__ == "__main__":
    main()