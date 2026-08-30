from pathlib import Path
import pandas as pd


TARGET_ROOTS = [
    Path("data/occupational_benchmark"),
    Path("results/occupational_benchmark_v6_job_roles_quick_models"),
    Path("results/occupational_benchmark_v6_job_roles_all_models"),
]


def patch_csv(path: Path):
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return False

    changed = False

    if "department" in df.columns and "field" not in df.columns:
        df["field"] = df["department"]
        changed = True

    if "role_key" in df.columns and "occupation_key" not in df.columns:
        df["occupation_key"] = df["role_key"]
        changed = True

    if changed:
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"Patched: {path}")

    return changed


def main():
    patched_count = 0

    for root in TARGET_ROOTS:
        if not root.exists():
            continue

        for path in root.rglob("*.csv"):
            if patch_csv(path):
                patched_count += 1

    print("")
    print(f"Total patched files: {patched_count}")


if __name__ == "__main__":
    main()