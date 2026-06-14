from pathlib import Path
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="CSV file to inspect.",
    )

    parser.add_argument(
        "--n",
        type=int,
        default=5,
        help="Number of rows to preview.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    df = pd.read_csv(input_path, encoding="utf-8-sig")

    print("Dataset:", input_path)
    print("Shape:", df.shape)

    print("\nColumns:")
    for col in df.columns:
        print("-", col)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nPreview:")
    print(df.head(args.n).to_string())


if __name__ == "__main__":
    main()