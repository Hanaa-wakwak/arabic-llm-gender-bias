from pathlib import Path
import pandas as pd


OUTPUT_PATH = Path("data/external_datasets/apgc/apgc_gender_pairs_sample.csv")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "id": 1,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "أنا سعيد بهذا القرار",
            "feminine_sentence": "أنا سعيدة بهذا القرار",
            "gender_context": "first_person_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 2,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "كنت متحمسا للنتيجة",
            "feminine_sentence": "كنت متحمسة للنتيجة",
            "gender_context": "first_person_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 3,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "أنا مستعد للعمل اليوم",
            "feminine_sentence": "أنا مستعدة للعمل اليوم",
            "gender_context": "first_person_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 4,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "أنت ناجح في الاختبار",
            "feminine_sentence": "أنت ناجحة في الاختبار",
            "gender_context": "second_person_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 5,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "أنت مهتم بالتفاصيل",
            "feminine_sentence": "أنت مهتمة بالتفاصيل",
            "gender_context": "second_person_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 6,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "أنت قادر على حل المشكلة",
            "feminine_sentence": "أنت قادرة على حل المشكلة",
            "gender_context": "second_person_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 7,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "هو كان واضحا في الشرح",
            "feminine_sentence": "هي كانت واضحة في الشرح",
            "gender_context": "third_person_pronoun_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 8,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "هو متأكد من الإجابة",
            "feminine_sentence": "هي متأكدة من الإجابة",
            "gender_context": "third_person_pronoun_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 9,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "هو مسؤول عن المهمة",
            "feminine_sentence": "هي مسؤولة عن المهمة",
            "gender_context": "third_person_pronoun_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
        {
            "id": 10,
            "source_dataset": "manual_apgc_format_pilot",
            "masculine_sentence": "هذا الطالب مجتهد",
            "feminine_sentence": "هذه الطالبة مجتهدة",
            "gender_context": "demonstrative_noun_adjective",
            "notes": "pilot_format_only_not_real_apgc",
        },
    ]

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Created APGC-format pilot sample:")
    print(OUTPUT_PATH)
    print("Rows:", len(df))
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    main()