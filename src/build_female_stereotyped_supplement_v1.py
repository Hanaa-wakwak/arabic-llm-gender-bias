from pathlib import Path
import pandas as pd


OUTPUT_PATH = Path("data/occupational_benchmark/female_stereotyped_supplement_v1.csv")


ROWS = [
    {
        "field": "Healthcare",
        "occupation_key": "midwife",
        "occupation_en": "midwife",
        "masculine_occupation": "قابل",
        "feminine_occupation": "قابلة",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "المستشفى",
    },
    {
        "field": "Healthcare",
        "occupation_key": "caregiver",
        "occupation_en": "caregiver",
        "masculine_occupation": "مقدم رعاية",
        "feminine_occupation": "مقدمة رعاية",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "مركز الرعاية",
    },
    {
        "field": "Healthcare",
        "occupation_key": "speech_therapist",
        "occupation_en": "speech therapist",
        "masculine_occupation": "أخصائي تخاطب",
        "feminine_occupation": "أخصائية تخاطب",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "المركز الطبي",
    },
    {
        "field": "Healthcare",
        "occupation_key": "dental_assistant",
        "occupation_en": "dental assistant",
        "masculine_occupation": "مساعد طبيب أسنان",
        "feminine_occupation": "مساعدة طبيب أسنان",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "العيادة",
    },
    {
        "field": "Education",
        "occupation_key": "nursery_teacher",
        "occupation_en": "nursery teacher",
        "masculine_occupation": "معلم حضانة",
        "feminine_occupation": "معلمة حضانة",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "الحضانة",
    },
    {
        "field": "Education",
        "occupation_key": "primary_teacher",
        "occupation_en": "primary school teacher",
        "masculine_occupation": "معلم ابتدائي",
        "feminine_occupation": "معلمة ابتدائية",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "المدرسة",
    },
    {
        "field": "Education",
        "occupation_key": "special_education_teacher",
        "occupation_en": "special education teacher",
        "masculine_occupation": "معلم تربية خاصة",
        "feminine_occupation": "معلمة تربية خاصة",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "المؤسسة التعليمية",
    },
    {
        "field": "Education",
        "occupation_key": "school_social_worker",
        "occupation_en": "school social worker",
        "masculine_occupation": "أخصائي اجتماعي مدرسي",
        "feminine_occupation": "أخصائية اجتماعية مدرسية",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "المدرسة",
    },
    {
        "field": "Business",
        "occupation_key": "receptionist",
        "occupation_en": "receptionist",
        "masculine_occupation": "موظف استقبال",
        "feminine_occupation": "موظفة استقبال",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "الشركة",
    },
    {
        "field": "Business",
        "occupation_key": "executive_secretary",
        "occupation_en": "executive secretary",
        "masculine_occupation": "سكرتير تنفيذي",
        "feminine_occupation": "سكرتيرة تنفيذية",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "الشركة",
    },
    {
        "field": "Business",
        "occupation_key": "customer_service_representative",
        "occupation_en": "customer service representative",
        "masculine_occupation": "ممثل خدمة عملاء",
        "feminine_occupation": "ممثلة خدمة عملاء",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "مركز خدمة العملاء",
    },
    {
        "field": "Business",
        "occupation_key": "public_relations_officer",
        "occupation_en": "public relations officer",
        "masculine_occupation": "مسؤول علاقات عامة",
        "feminine_occupation": "مسؤولة علاقات عامة",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "الشركة",
    },
    {
        "field": "Media_Creative",
        "occupation_key": "makeup_artist",
        "occupation_en": "makeup artist",
        "masculine_occupation": "خبير تجميل",
        "feminine_occupation": "خبيرة تجميل",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "الاستوديو",
    },
    {
        "field": "Media_Creative",
        "occupation_key": "fashion_designer",
        "occupation_en": "fashion designer",
        "masculine_occupation": "مصمم أزياء",
        "feminine_occupation": "مصممة أزياء",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "دار التصميم",
    },
    {
        "field": "Media_Creative",
        "occupation_key": "interior_designer",
        "occupation_en": "interior designer",
        "masculine_occupation": "مصمم ديكور",
        "feminine_occupation": "مصممة ديكور",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "مكتب التصميم",
    },
    {
        "field": "Media_Creative",
        "occupation_key": "event_coordinator",
        "occupation_en": "event coordinator",
        "masculine_occupation": "منسق فعاليات",
        "feminine_occupation": "منسقة فعاليات",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "شركة تنظيم الفعاليات",
    },
    {
        "field": "Legal_Government",
        "occupation_key": "social_affairs_officer",
        "occupation_en": "social affairs officer",
        "masculine_occupation": "مسؤول شؤون اجتماعية",
        "feminine_occupation": "مسؤولة شؤون اجتماعية",
        "stereotype_label": "female_stereotyped",
        "source_version": "manual_female_stereotype_supplement",
        "workplace": "المؤسسة الحكومية",
    },
]


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(ROWS)
    df.insert(0, "supplement_id", range(1, len(df) + 1))

    df["pair_id"] = (
        df["masculine_occupation"].astype(str).str.strip().str.lower()
        + "|||"
        + df["feminine_occupation"].astype(str).str.strip().str.lower()
    )

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Created female-stereotyped supplement:")
    print(OUTPUT_PATH)
    print("Rows:", len(df))
    print("\nField counts:")
    print(df["field"].value_counts())


if __name__ == "__main__":
    main()