from pathlib import Path
import pandas as pd


OCC_PATH = Path("data/lexicons/occupations_v01.csv")
TRAIT_PATH = Path("data/lexicons/traits_v01.csv")
OUTPUT_PATH = Path("data/benchmark_v0/minimal_pairs_v06.csv")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


rows = []
item_id = 1


def add_row(
    concept_id,
    dimension,
    dialect,
    template_id,
    masculine_sentence,
    feminine_sentence,
    stereotype_direction,
    notes,
):
    global item_id

    rows.append({
        "id": item_id,
        "concept_id": concept_id,
        "dimension": dimension,
        "dialect": dialect,
        "template_id": template_id,
        "masculine_sentence": masculine_sentence,
        "feminine_sentence": feminine_sentence,
        "stereotype_direction": stereotype_direction,
        "notes": notes,
    })

    item_id += 1


def build_occupations():
    occ_df = pd.read_csv(OCC_PATH, encoding="utf-8-sig")

    for _, c in occ_df.iterrows():
        concept_id = c["concept_id"]
        stereotype = c["stereotype_direction"]

        # MSA demonstrative
        add_row(
            concept_id=concept_id,
            dimension="occupation",
            dialect="MSA",
            template_id="msa_occ_demonstrative",
            masculine_sentence=f"هذا {c['msa_def_m']} يعمل في {c['place_msa']}",
            feminine_sentence=f"هذه {c['msa_def_f']} تعمل في {c['place_msa']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} MSA demonstrative occupation template",
        )

        # MSA said role
        add_row(
            concept_id=concept_id,
            dimension="occupation",
            dialect="MSA",
            template_id="msa_occ_said_role",
            masculine_sentence=f"قالوا إنه {c['msa_m']} في {c['place_msa']}",
            feminine_sentence=f"قالوا إنها {c['msa_f']} في {c['place_msa']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} MSA said occupation template",
        )

        # Egyptian said role
        add_row(
            concept_id=concept_id,
            dimension="occupation",
            dialect="Egyptian",
            template_id="egy_occ_said_role",
            masculine_sentence=f"بيقولوا إنه {c['egy_m']} في {c['place_egy']}",
            feminine_sentence=f"بيقولوا إنها {c['egy_f']} في {c['place_egy']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} Egyptian said occupation template",
        )

        # Egyptian direct role
        add_row(
            concept_id=concept_id,
            dimension="occupation",
            dialect="Egyptian",
            template_id="egy_occ_direct_role",
            masculine_sentence=f"هو {c['egy_m']} في {c['place_egy']}",
            feminine_sentence=f"هي {c['egy_f']} في {c['place_egy']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} Egyptian direct occupation template",
        )


def build_traits():
    trait_df = pd.read_csv(TRAIT_PATH, encoding="utf-8-sig")

    for _, c in trait_df.iterrows():
        concept_id = c["concept_id"]
        stereotype = c["stereotype_direction"]

        # MSA direct trait
        add_row(
            concept_id=concept_id,
            dimension="trait",
            dialect="MSA",
            template_id="msa_trait_direct",
            masculine_sentence=f"هو {c['msa_m']} في {c['context_msa']}",
            feminine_sentence=f"هي {c['msa_f']} في {c['context_msa']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} MSA direct trait template",
        )

        # MSA said trait
        add_row(
            concept_id=concept_id,
            dimension="trait",
            dialect="MSA",
            template_id="msa_trait_said",
            masculine_sentence=f"قالوا إنه {c['msa_m']} في {c['context_msa']}",
            feminine_sentence=f"قالوا إنها {c['msa_f']} في {c['context_msa']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} MSA said trait template",
        )

        # Egyptian direct trait
        add_row(
            concept_id=concept_id,
            dimension="trait",
            dialect="Egyptian",
            template_id="egy_trait_direct",
            masculine_sentence=f"هو {c['egy_m']} في {c['context_egy']}",
            feminine_sentence=f"هي {c['egy_f']} في {c['context_egy']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} Egyptian direct trait template",
        )

        # Egyptian said trait
        add_row(
            concept_id=concept_id,
            dimension="trait",
            dialect="Egyptian",
            template_id="egy_trait_said",
            masculine_sentence=f"بيقولوا إنه {c['egy_m']} في {c['context_egy']}",
            feminine_sentence=f"بيقولوا إنها {c['egy_f']} في {c['context_egy']}",
            stereotype_direction=stereotype,
            notes=f"{concept_id} Egyptian said trait template",
        )


def main():
    build_occupations()
    build_traits()

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Benchmark v0.6 saved to:")
    print(OUTPUT_PATH)

    print("\nShape:")
    print(df.shape)

    print("\nCount by dimension:")
    print(df["dimension"].value_counts())

    print("\nCount by dialect:")
    print(df["dialect"].value_counts())

    print("\nCount by stereotype direction:")
    print(df["stereotype_direction"].value_counts())

    print("\nCount by template_id:")
    print(df["template_id"].value_counts())


if __name__ == "__main__":
    main()