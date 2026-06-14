from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Original APGC CSV file.",
    )

    parser.add_argument(
        "--output",
        default="data/external_datasets/apgc/apgc_gender_pairs_real.csv",
        help="Output file in thesis pairwise format.",
    )

    parser.add_argument(
        "--masculine_col",
        required=True,
        help="Column name containing masculine sentence variant.",
    )

    parser.add_argument(
        "--feminine_col",
        required=True,
        help="Column name containing feminine sentence variant.",
    )

    parser.add_argument(
        "--context_col",
        default=None,
        help="Optional column name containing gender/context label.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of rows to convert.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    required = [args.masculine_col, args.feminine_col]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    if args.context_col and args.context_col not in df.columns:
        raise ValueError(
            f"Context column not found: {args.context_col}\n"
            f"Available columns: {list(df.columns)}"
        )

    df = df.dropna(subset=[args.masculine_col, args.feminine_col]).copy()

    if args.limit:
        df = df.head(args.limit)

    rows = []

    for idx, row in df.iterrows():
        masculine_sentence = str(row[args.masculine_col]).strip()
        feminine_sentence = str(row[args.feminine_col]).strip()

        if not masculine_sentence or not feminine_sentence:
            continue

        gender_context = (
            str(row[args.context_col]).strip()
            if args.context_col
            else "apgc_unspecified_context"
        )

        rows.append({
            "id": len(rows) + 1,
            "source_dataset": "APGC",
            "masculine_sentence": masculine_sentence,
            "feminine_sentence": feminine_sentence,
            "gender_context": gender_context,
            "notes": "converted_from_real_apgc",
        })

    output_df = pd.DataFrame(rows)

    output_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("APGC conversion completed.")
    print("Input:", input_path)
    print("Output:", output_path)
    print("Rows:", len(output_df))
    print("Columns:", list(output_df.columns))


if __name__ == "__main__":
    main()