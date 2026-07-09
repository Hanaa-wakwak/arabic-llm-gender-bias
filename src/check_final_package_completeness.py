from pathlib import Path
import pandas as pd


REGISTRY_PATH = Path("results/final_package/final_artifact_registry.csv")
OUTPUT_PATH = Path("results/final_package/final_package_completeness_check.csv")


def main():
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(
            f"Registry file not found: {REGISTRY_PATH}. "
            "Run src/create_final_artifact_registry.py first."
        )

    df = pd.read_csv(REGISTRY_PATH, encoding="utf-8-sig")

    missing_df = df[df["exists"] == False].copy()
    existing_df = df[df["exists"] == True].copy()

    summary_df = pd.DataFrame([
        {"metric": "tracked_artifacts", "value": len(df)},
        {"metric": "existing_artifacts", "value": len(existing_df)},
        {"metric": "missing_artifacts", "value": len(missing_df)},
        {"metric": "package_complete", "value": len(missing_df) == 0},
    ])

    summary_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("Final package completeness check completed.")
    print("Output:", OUTPUT_PATH)
    print(summary_df.to_string(index=False))

    if len(missing_df) > 0:
        print("\nMissing artifacts:")
        print(missing_df[["artifact_type", "description", "path"]].to_string(index=False))
        raise SystemExit(1)

    print("\nFinal package is complete.")


if __name__ == "__main__":
    main()