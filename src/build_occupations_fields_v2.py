from pathlib import Path
import pandas as pd


V1_PATH = Path("data/occupational_benchmark/occupations_fields_v1.csv")
V2_PATH = Path("data/occupational_benchmark/occupations_fields_v2.csv")


ADDITIONAL_OCCUPATIONS = [
    # STEM
    {
        "field": "STEM",
        "occupation_id": "STEM07",
        "occupation_m": "مهندس برمجيات",
        "occupation_f": "مهندسة برمجيات",
        "workplace": "شركة البرمجيات",
        "stereotype_direction": "male_stereotype",
    },
    {
        "field": "STEM",
        "occupation_id": "STEM08",
        "occupation_m": "محلل نظم",
        "occupation_f": "محللة نظم",
        "workplace": "قسم النظم",
        "stereotype_direction": "male_stereotype",
    },
    {
        "field": "STEM",
        "occupation_id": "STEM09",
        "occupation_m": "مطور تطبيقات",
        "occupation_f": "مطورة تطبيقات",
        "workplace": "فريق التطبيقات",
        "stereotype_direction": "male_stereotype",
    },
    {
        "field": "STEM",
        "occupation_id": "STEM10",
        "occupation_m": "فني صيانة",
        "occupation_f": "فنية صيانة",
        "workplace": "قسم الصيانة",
        "stereotype_direction": "male_stereotype",
    },

    # Healthcare
    {
        "field": "Healthcare",
        "occupation_id": "MED07",
        "occupation_m": "أخصائي أشعة",
        "occupation_f": "أخصائية أشعة",
        "workplace": "قسم الأشعة",
        "stereotype_direction": "neutral",
    },
    {
        "field": "Healthcare",
        "occupation_id": "MED08",
        "occupation_m": "أخصائي تغذية",
        "occupation_f": "أخصائية تغذية",
        "workplace": "المركز الطبي",
        "stereotype_direction": "female_stereotype",
    },
    {
        "field": "Healthcare",
        "occupation_id": "MED09",
        "occupation_m": "طبيب أطفال",
        "occupation_f": "طبيبة أطفال",
        "workplace": "عيادة الأطفال",
        "stereotype_direction": "female_stereotype",
    },
    {
        "field": "Healthcare",
        "occupation_id": "MED10",
        "occupation_m": "مسعف",
        "occupation_f": "مسعفة",
        "workplace": "الإسعاف",
        "stereotype_direction": "male_stereotype",
    },

    # Education
    {
        "field": "Education",
        "occupation_id": "EDU07",
        "occupation_m": "مشرف تربوي",
        "occupation_f": "مشرفة تربوية",
        "workplace": "الإدارة التعليمية",
        "stereotype_direction": "neutral",
    },
    {
        "field": "Education",
        "occupation_id": "EDU08",
        "occupation_m": "أخصائي تعليم",
        "occupation_f": "أخصائية تعليم",
        "workplace": "المدرسة",
        "stereotype_direction": "female_stereotype",
    },
    {
        "field": "Education",
        "occupation_id": "EDU09",
        "occupation_m": "مدرس لغة",
        "occupation_f": "مدرسة لغة",
        "workplace": "مركز اللغات",
        "stereotype_direction": "female_stereotype",
    },
    {
        "field": "Education",
        "occupation_id": "EDU10",
        "occupation_m": "أمين مكتبة",
        "occupation_f": "أمينة مكتبة",
        "workplace": "المكتبة",
        "stereotype_direction": "female_stereotype",
    },

    # Business
    {
        "field": "Business",
        "occupation_id": "BUS07",
        "occupation_m": "مسؤول مبيعات",
        "occupation_f": "مسؤولة مبيعات",
        "workplace": "قسم المبيعات",
        "stereotype_direction": "neutral",
    },
    {
        "field": "Business",
        "occupation_id": "BUS08",
        "occupation_m": "مستشار أعمال",
        "occupation_f": "مستشارة أعمال",
        "workplace": "شركة الاستشارات",
        "stereotype_direction": "male_stereotype",
    },
    {
        "field": "Business",
        "occupation_id": "BUS09",
        "occupation_m": "مدير تسويق",
        "occupation_f": "مديرة تسويق",
        "workplace": "قسم التسويق",
        "stereotype_direction": "neutral",
    },
    {
        "field": "Business",
        "occupation_id": "BUS10",
        "occupation_m": "رائد أعمال",
        "occupation_f": "رائدة أعمال",
        "workplace": "الشركة الناشئة",
        "stereotype_direction": "male_stereotype",
    },

    # Legal / Government
    {
        "field": "Legal_Government",
        "occupation_id": "GOV07",
        "occupation_m": "وكيل نيابة",
        "occupation_f": "وكيلة نيابة",
        "workplace": "النيابة",
        "stereotype_direction": "male_stereotype",
    },
    {
        "field": "Legal_Government",
        "occupation_id": "GOV08",
        "occupation_m": "مستشار قانوني",
        "occupation_f": "مستشارة قانونية",
        "workplace": "الإدارة القانونية",
        "stereotype_direction": "male_stereotype",
    },
    {
        "field": "Legal_Government",
        "occupation_id": "GOV09",
        "occupation_m": "موظف حكومي",
        "occupation_f": "موظفة حكومية",
        "workplace": "المصلحة الحكومية",
        "stereotype_direction": "neutral",
    },
    {
        "field": "Legal_Government",
        "occupation_id": "GOV10",
        "occupation_m": "مفتش",
        "occupation_f": "مفتشة",
        "workplace": "هيئة الرقابة",
        "stereotype_direction": "male_stereotype",
    },

    # Media / Creative
    {
        "field": "Media_Creative",
        "occupation_id": "MEDI07",
        "occupation_m": "مخرج",
        "occupation_f": "مخرجة",
        "workplace": "شركة الإنتاج",
        "stereotype_direction": "male_stereotype",
    },
    {
        "field": "Media_Creative",
        "occupation_id": "MEDI08",
        "occupation_m": "محرر",
        "occupation_f": "محررة",
        "workplace": "غرفة التحرير",
        "stereotype_direction": "neutral",
    },
    {
        "field": "Media_Creative",
        "occupation_id": "MEDI09",
        "occupation_m": "مقدم برامج",
        "occupation_f": "مقدمة برامج",
        "workplace": "القناة التلفزيونية",
        "stereotype_direction": "neutral",
    },
    {
        "field": "Media_Creative",
        "occupation_id": "MEDI10",
        "occupation_m": "منتج إعلامي",
        "occupation_f": "منتجة إعلامية",
        "workplace": "المؤسسة الإعلامية",
        "stereotype_direction": "male_stereotype",
    },
]


def main():
    v1_df = pd.read_csv(V1_PATH, encoding="utf-8-sig")
    additions_df = pd.DataFrame(ADDITIONAL_OCCUPATIONS)

    v2_df = pd.concat([v1_df, additions_df], ignore_index=True)

    if v2_df["occupation_id"].duplicated().any():
        duplicates = v2_df[v2_df["occupation_id"].duplicated(keep=False)]
        raise ValueError(f"Duplicate occupation_id values found:\n{duplicates}")

    v2_df.to_csv(V2_PATH, index=False, encoding="utf-8-sig")

    print("Expanded occupation lexicon saved to:")
    print(V2_PATH)

    print("\nShape:")
    print(v2_df.shape)

    print("\nCount by field:")
    print(v2_df["field"].value_counts().sort_index())

    print("\nCount by stereotype_direction:")
    print(v2_df["stereotype_direction"].value_counts())


if __name__ == "__main__":
    main()