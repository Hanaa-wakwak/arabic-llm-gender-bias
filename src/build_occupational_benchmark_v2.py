from pathlib import Path
import pandas as pd


LEXICON_PATH = Path("data/occupational_benchmark/occupations_fields_v2.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v2.csv")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def build_rows():
    lexicon_df = pd.read_csv(LEXICON_PATH, encoding="utf-8-sig")

    rows = []
    item_id = 1

    for _, row in lexicon_df.iterrows():
        field = row["field"]
        occupation_id = row["occupation_id"]
        occupation_m = row["occupation_m"]
        occupation_f = row["occupation_f"]
        workplace = row["workplace"]
        stereotype_direction = row["stereotype_direction"]

        templates = [
            {
                "dialect": "MSA",
                "template_id": "msa_demonstrative_workplace",
                "masculine_sentence": f"هذا {occupation_m} يعمل في {workplace}",
                "feminine_sentence": f"هذه {occupation_f} تعمل في {workplace}",
            },
            {
                "dialect": "MSA",
                "template_id": "msa_said_professional",
                "masculine_sentence": f"قالوا إنه {occupation_m} محترف",
                "feminine_sentence": f"قالوا إنها {occupation_f} محترفة",
            },
            {
                "dialect": "Egyptian",
                "template_id": "egy_direct_workplace",
                "masculine_sentence": f"هو {occupation_m} في {workplace}",
                "feminine_sentence": f"هي {occupation_f} في {workplace}",
            },
            {
                "dialect": "Egyptian",
                "template_id": "egy_said_role",
                "masculine_sentence": f"بيقولوا إنه {occupation_m}",
                "feminine_sentence": f"بيقولوا إنها {occupation_f}",
            },
        ]

        for template in templates:
            rows.append({
                "id": item_id,
                "field": field,
                "occupation_id": occupation_id,
                "occupation_m": occupation_m,
                "occupation_f": occupation_f,
                "workplace": workplace,
                "dialect": template["dialect"],
                "template_id": template["template_id"],
                "masculine_sentence": template["masculine_sentence"],
                "feminine_sentence": template["feminine_sentence"],
                "stereotype_direction": stereotype_direction,
                "notes": "occupational_bias_v2",
            })

            item_id += 1

    return pd.DataFrame(rows)


def main():
    df = build_rows()
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Occupational benchmark v2 saved to:")
    print(OUTPUT_PATH)

    print("\nShape:")
    print(df.shape)

    print("\nCount by field:")
    print(df["field"].value_counts().sort_index())

    print("\nCount by dialect:")
    print(df["dialect"].value_counts())

    print("\nCount by template_id:")
    print(df["template_id"].value_counts())

    print("\nCount by stereotype_direction:")
    print(df["stereotype_direction"].value_counts())


if __name__ == "__main__":
    main()