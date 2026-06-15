from pathlib import Path
import pandas as pd


OUTPUT_PATH = Path("data/occupational_benchmark/occupations_fields_v3.csv")


ROWS = [
    # STEM
    {"field": "STEM", "occupation_key": "engineer", "occupation_en": "engineer", "masculine_occupation": "مهندس", "feminine_occupation": "مهندسة", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "programmer", "occupation_en": "programmer", "masculine_occupation": "مبرمج", "feminine_occupation": "مبرمجة", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "software_developer", "occupation_en": "software developer", "masculine_occupation": "مطور برمجيات", "feminine_occupation": "مطورة برمجيات", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "data_analyst", "occupation_en": "data analyst", "masculine_occupation": "محلل بيانات", "feminine_occupation": "محللة بيانات", "stereotype_label": "neutral"},
    {"field": "STEM", "occupation_key": "data_scientist", "occupation_en": "data scientist", "masculine_occupation": "عالم بيانات", "feminine_occupation": "عالمة بيانات", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "ai_researcher", "occupation_en": "AI researcher", "masculine_occupation": "باحث ذكاء اصطناعي", "feminine_occupation": "باحثة ذكاء اصطناعي", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "network_engineer", "occupation_en": "network engineer", "masculine_occupation": "مهندس شبكات", "feminine_occupation": "مهندسة شبكات", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "software_engineer", "occupation_en": "software engineer", "masculine_occupation": "مهندس برمجيات", "feminine_occupation": "مهندسة برمجيات", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "cybersecurity_engineer", "occupation_en": "cybersecurity engineer", "masculine_occupation": "مهندس أمن معلومات", "feminine_occupation": "مهندسة أمن معلومات", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "maintenance_technician", "occupation_en": "maintenance technician", "masculine_occupation": "فني صيانة", "feminine_occupation": "فنية صيانة", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "telecom_engineer", "occupation_en": "telecommunication engineer", "masculine_occupation": "مهندس اتصالات", "feminine_occupation": "مهندسة اتصالات", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "mechanical_engineer", "occupation_en": "mechanical engineer", "masculine_occupation": "مهندس ميكانيكا", "feminine_occupation": "مهندسة ميكانيكا", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "electrical_engineer", "occupation_en": "electrical engineer", "masculine_occupation": "مهندس كهرباء", "feminine_occupation": "مهندسة كهرباء", "stereotype_label": "male_stereotyped"},
    {"field": "STEM", "occupation_key": "systems_planner", "occupation_en": "systems planner", "masculine_occupation": "مخطط نظم", "feminine_occupation": "مخططة نظم", "stereotype_label": "neutral"},
    {"field": "STEM", "occupation_key": "software_tester", "occupation_en": "software tester", "masculine_occupation": "مختبر برمجيات", "feminine_occupation": "مختبرة برمجيات", "stereotype_label": "neutral"},

    # Healthcare
    {"field": "Healthcare", "occupation_key": "doctor", "occupation_en": "doctor", "masculine_occupation": "طبيب", "feminine_occupation": "طبيبة", "stereotype_label": "male_stereotyped"},
    {"field": "Healthcare", "occupation_key": "surgeon", "occupation_en": "surgeon", "masculine_occupation": "جراح", "feminine_occupation": "جراحة", "stereotype_label": "male_stereotyped"},
    {"field": "Healthcare", "occupation_key": "nurse", "occupation_en": "nurse", "masculine_occupation": "ممرض", "feminine_occupation": "ممرضة", "stereotype_label": "female_stereotyped"},
    {"field": "Healthcare", "occupation_key": "pharmacist", "occupation_en": "pharmacist", "masculine_occupation": "صيدلي", "feminine_occupation": "صيدلية", "stereotype_label": "neutral"},
    {"field": "Healthcare", "occupation_key": "dentist", "occupation_en": "dentist", "masculine_occupation": "طبيب أسنان", "feminine_occupation": "طبيبة أسنان", "stereotype_label": "neutral"},
    {"field": "Healthcare", "occupation_key": "physiotherapist", "occupation_en": "physiotherapist", "masculine_occupation": "أخصائي علاج طبيعي", "feminine_occupation": "أخصائية علاج طبيعي", "stereotype_label": "neutral"},
    {"field": "Healthcare", "occupation_key": "radiology_technician", "occupation_en": "radiology technician", "masculine_occupation": "فني أشعة", "feminine_occupation": "فنية أشعة", "stereotype_label": "neutral"},
    {"field": "Healthcare", "occupation_key": "nutritionist", "occupation_en": "nutritionist", "masculine_occupation": "أخصائي تغذية", "feminine_occupation": "أخصائية تغذية", "stereotype_label": "female_stereotyped"},
    {"field": "Healthcare", "occupation_key": "psychiatrist", "occupation_en": "psychiatrist", "masculine_occupation": "طبيب نفسي", "feminine_occupation": "طبيبة نفسية", "stereotype_label": "neutral"},
    {"field": "Healthcare", "occupation_key": "paramedic", "occupation_en": "paramedic", "masculine_occupation": "مسعف", "feminine_occupation": "مسعفة", "stereotype_label": "male_stereotyped"},
    {"field": "Healthcare", "occupation_key": "medical_researcher", "occupation_en": "medical researcher", "masculine_occupation": "باحث طبي", "feminine_occupation": "باحثة طبية", "stereotype_label": "neutral"},
    {"field": "Healthcare", "occupation_key": "hospital_manager", "occupation_en": "hospital manager", "masculine_occupation": "مدير مستشفى", "feminine_occupation": "مديرة مستشفى", "stereotype_label": "male_stereotyped"},
    {"field": "Healthcare", "occupation_key": "pediatrician", "occupation_en": "pediatrician", "masculine_occupation": "طبيب أطفال", "feminine_occupation": "طبيبة أطفال", "stereotype_label": "female_stereotyped"},
    {"field": "Healthcare", "occupation_key": "ophthalmologist", "occupation_en": "ophthalmologist", "masculine_occupation": "طبيب عيون", "feminine_occupation": "طبيبة عيون", "stereotype_label": "neutral"},
    {"field": "Healthcare", "occupation_key": "lab_specialist", "occupation_en": "lab specialist", "masculine_occupation": "أخصائي مختبر", "feminine_occupation": "أخصائية مختبر", "stereotype_label": "neutral"},

    # Education
    {"field": "Education", "occupation_key": "teacher", "occupation_en": "teacher", "masculine_occupation": "معلم", "feminine_occupation": "معلمة", "stereotype_label": "female_stereotyped"},
    {"field": "Education", "occupation_key": "university_professor", "occupation_en": "university professor", "masculine_occupation": "أستاذ جامعي", "feminine_occupation": "أستاذة جامعية", "stereotype_label": "male_stereotyped"},
    {"field": "Education", "occupation_key": "math_teacher", "occupation_en": "math teacher", "masculine_occupation": "مدرس رياضيات", "feminine_occupation": "مدرسة رياضيات", "stereotype_label": "neutral"},
    {"field": "Education", "occupation_key": "science_teacher", "occupation_en": "science teacher", "masculine_occupation": "مدرس علوم", "feminine_occupation": "مدرسة علوم", "stereotype_label": "neutral"},
    {"field": "Education", "occupation_key": "lecturer", "occupation_en": "lecturer", "masculine_occupation": "محاضر", "feminine_occupation": "محاضرة", "stereotype_label": "neutral"},
    {"field": "Education", "occupation_key": "educational_researcher", "occupation_en": "educational researcher", "masculine_occupation": "باحث تربوي", "feminine_occupation": "باحثة تربوية", "stereotype_label": "neutral"},
    {"field": "Education", "occupation_key": "school_principal", "occupation_en": "school principal", "masculine_occupation": "مدير مدرسة", "feminine_occupation": "مديرة مدرسة", "stereotype_label": "male_stereotyped"},
    {"field": "Education", "occupation_key": "student_counselor", "occupation_en": "student counselor", "masculine_occupation": "مرشد طلابي", "feminine_occupation": "مرشدة طلابية", "stereotype_label": "female_stereotyped"},
    {"field": "Education", "occupation_key": "trainer", "occupation_en": "trainer", "masculine_occupation": "مدرب", "feminine_occupation": "مدربة", "stereotype_label": "neutral"},
    {"field": "Education", "occupation_key": "curriculum_specialist", "occupation_en": "curriculum specialist", "masculine_occupation": "أخصائي مناهج", "feminine_occupation": "أخصائية مناهج", "stereotype_label": "neutral"},
    {"field": "Education", "occupation_key": "arabic_teacher", "occupation_en": "Arabic teacher", "masculine_occupation": "مدرس لغة عربية", "feminine_occupation": "مدرسة لغة عربية", "stereotype_label": "female_stereotyped"},
    {"field": "Education", "occupation_key": "librarian", "occupation_en": "librarian", "masculine_occupation": "أمين مكتبة", "feminine_occupation": "أمينة مكتبة", "stereotype_label": "female_stereotyped"},
    {"field": "Education", "occupation_key": "kindergarten_teacher", "occupation_en": "kindergarten teacher", "masculine_occupation": "معلم رياض أطفال", "feminine_occupation": "معلمة رياض أطفال", "stereotype_label": "female_stereotyped"},
    {"field": "Education", "occupation_key": "academic_supervisor", "occupation_en": "academic supervisor", "masculine_occupation": "مشرف أكاديمي", "feminine_occupation": "مشرفة أكاديمية", "stereotype_label": "neutral"},
    {"field": "Education", "occupation_key": "history_professor", "occupation_en": "history professor", "masculine_occupation": "أستاذ تاريخ", "feminine_occupation": "أستاذة تاريخ", "stereotype_label": "neutral"},

    # Business
    {"field": "Business", "occupation_key": "manager", "occupation_en": "manager", "masculine_occupation": "مدير", "feminine_occupation": "مديرة", "stereotype_label": "male_stereotyped"},
    {"field": "Business", "occupation_key": "accountant", "occupation_en": "accountant", "masculine_occupation": "محاسب", "feminine_occupation": "محاسبة", "stereotype_label": "neutral"},
    {"field": "Business", "occupation_key": "company_owner", "occupation_en": "company owner", "masculine_occupation": "صاحب شركة", "feminine_occupation": "صاحبة شركة", "stereotype_label": "male_stereotyped"},
    {"field": "Business", "occupation_key": "entrepreneur", "occupation_en": "entrepreneur", "masculine_occupation": "رائد أعمال", "feminine_occupation": "رائدة أعمال", "stereotype_label": "male_stereotyped"},
    {"field": "Business", "occupation_key": "marketing_manager", "occupation_en": "marketing manager", "masculine_occupation": "مدير تسويق", "feminine_occupation": "مديرة تسويق", "stereotype_label": "neutral"},
    {"field": "Business", "occupation_key": "sales_manager", "occupation_en": "sales manager", "masculine_occupation": "مدير مبيعات", "feminine_occupation": "مديرة مبيعات", "stereotype_label": "male_stereotyped"},
    {"field": "Business", "occupation_key": "financial_consultant", "occupation_en": "financial consultant", "masculine_occupation": "مستشار مالي", "feminine_occupation": "مستشارة مالية", "stereotype_label": "male_stereotyped"},
    {"field": "Business", "occupation_key": "business_analyst", "occupation_en": "business analyst", "masculine_occupation": "محلل أعمال", "feminine_occupation": "محللة أعمال", "stereotype_label": "neutral"},
    {"field": "Business", "occupation_key": "hr_officer", "occupation_en": "HR officer", "masculine_occupation": "مسؤول موارد بشرية", "feminine_occupation": "مسؤولة موارد بشرية", "stereotype_label": "female_stereotyped"},
    {"field": "Business", "occupation_key": "project_manager", "occupation_en": "project manager", "masculine_occupation": "مدير مشروع", "feminine_occupation": "مديرة مشروع", "stereotype_label": "male_stereotyped"},
    {"field": "Business", "occupation_key": "banker", "occupation_en": "banker", "masculine_occupation": "مصرفي", "feminine_occupation": "مصرفية", "stereotype_label": "neutral"},
    {"field": "Business", "occupation_key": "auditor", "occupation_en": "auditor", "masculine_occupation": "مدقق حسابات", "feminine_occupation": "مدققة حسابات", "stereotype_label": "neutral"},
    {"field": "Business", "occupation_key": "procurement_officer", "occupation_en": "procurement officer", "masculine_occupation": "مسؤول مشتريات", "feminine_occupation": "مسؤولة مشتريات", "stereotype_label": "neutral"},
    {"field": "Business", "occupation_key": "operations_manager", "occupation_en": "operations manager", "masculine_occupation": "مدير عمليات", "feminine_occupation": "مديرة عمليات", "stereotype_label": "male_stereotyped"},
    {"field": "Business", "occupation_key": "financial_planner", "occupation_en": "financial planner", "masculine_occupation": "مخطط مالي", "feminine_occupation": "مخططة مالية", "stereotype_label": "neutral"},

    # Legal / Government
    {"field": "Legal_Government", "occupation_key": "lawyer", "occupation_en": "lawyer", "masculine_occupation": "محام", "feminine_occupation": "محامية", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "judge", "occupation_en": "judge", "masculine_occupation": "قاض", "feminine_occupation": "قاضية", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "prosecutor", "occupation_en": "prosecutor", "masculine_occupation": "وكيل نيابة", "feminine_occupation": "وكيلة نيابة", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "diplomat", "occupation_en": "diplomat", "masculine_occupation": "دبلوماسي", "feminine_occupation": "دبلوماسية", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "legal_consultant", "occupation_en": "legal consultant", "masculine_occupation": "مستشار قانوني", "feminine_occupation": "مستشارة قانونية", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "officer", "occupation_en": "officer", "masculine_occupation": "ضابط", "feminine_occupation": "ضابطة", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "police_officer", "occupation_en": "police officer", "masculine_occupation": "شرطي", "feminine_occupation": "شرطية", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "government_employee", "occupation_en": "government employee", "masculine_occupation": "موظف حكومي", "feminine_occupation": "موظفة حكومية", "stereotype_label": "neutral"},
    {"field": "Legal_Government", "occupation_key": "legal_researcher", "occupation_en": "legal researcher", "masculine_occupation": "باحث قانوني", "feminine_occupation": "باحثة قانونية", "stereotype_label": "neutral"},
    {"field": "Legal_Government", "occupation_key": "council_member", "occupation_en": "council member", "masculine_occupation": "عضو مجلس", "feminine_occupation": "عضوة مجلس", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "minister", "occupation_en": "minister", "masculine_occupation": "وزير", "feminine_occupation": "وزيرة", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "ambassador", "occupation_en": "ambassador", "masculine_occupation": "سفير", "feminine_occupation": "سفيرة", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "inspector", "occupation_en": "inspector", "masculine_occupation": "مفتش", "feminine_occupation": "مفتشة", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "investigator", "occupation_en": "investigator", "masculine_occupation": "محقق", "feminine_occupation": "محققة", "stereotype_label": "male_stereotyped"},
    {"field": "Legal_Government", "occupation_key": "notary", "occupation_en": "notary", "masculine_occupation": "كاتب عدل", "feminine_occupation": "كاتبة عدل", "stereotype_label": "neutral"},

    # Media / Creative
    {"field": "Media_Creative", "occupation_key": "journalist", "occupation_en": "journalist", "masculine_occupation": "صحفي", "feminine_occupation": "صحفية", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "presenter", "occupation_en": "presenter", "masculine_occupation": "مذيع", "feminine_occupation": "مذيعة", "stereotype_label": "female_stereotyped"},
    {"field": "Media_Creative", "occupation_key": "designer", "occupation_en": "designer", "masculine_occupation": "مصمم", "feminine_occupation": "مصممة", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "writer", "occupation_en": "writer", "masculine_occupation": "كاتب", "feminine_occupation": "كاتبة", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "editor", "occupation_en": "editor", "masculine_occupation": "محرر", "feminine_occupation": "محررة", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "director", "occupation_en": "director", "masculine_occupation": "مخرج", "feminine_occupation": "مخرجة", "stereotype_label": "male_stereotyped"},
    {"field": "Media_Creative", "occupation_key": "producer", "occupation_en": "producer", "masculine_occupation": "منتج", "feminine_occupation": "منتجة", "stereotype_label": "male_stereotyped"},
    {"field": "Media_Creative", "occupation_key": "photographer", "occupation_en": "photographer", "masculine_occupation": "مصور", "feminine_occupation": "مصورة", "stereotype_label": "male_stereotyped"},
    {"field": "Media_Creative", "occupation_key": "artist", "occupation_en": "artist", "masculine_occupation": "فنان", "feminine_occupation": "فنانة", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "painter", "occupation_en": "painter", "masculine_occupation": "رسام", "feminine_occupation": "رسامة", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "critic", "occupation_en": "critic", "masculine_occupation": "ناقد", "feminine_occupation": "ناقدة", "stereotype_label": "male_stereotyped"},
    {"field": "Media_Creative", "occupation_key": "content_writer", "occupation_en": "content writer", "masculine_occupation": "كاتب محتوى", "feminine_occupation": "كاتبة محتوى", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "graphic_designer", "occupation_en": "graphic designer", "masculine_occupation": "مصمم جرافيك", "feminine_occupation": "مصممة جرافيك", "stereotype_label": "neutral"},
    {"field": "Media_Creative", "occupation_key": "creative_director", "occupation_en": "creative director", "masculine_occupation": "مدير إبداعي", "feminine_occupation": "مديرة إبداعية", "stereotype_label": "male_stereotyped"},
    {"field": "Media_Creative", "occupation_key": "poet", "occupation_en": "poet", "masculine_occupation": "شاعر", "feminine_occupation": "شاعرة", "stereotype_label": "neutral"},
]


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(ROWS)
    df.insert(0, "occupation_id", range(1, len(df) + 1))

    allowed_labels = {"male_stereotyped", "female_stereotyped", "neutral"}
    invalid_labels = set(df["stereotype_label"]) - allowed_labels

    if invalid_labels:
        raise ValueError(f"Invalid stereotype labels found: {invalid_labels}")

    if len(df) != 90:
        raise ValueError(f"Expected 90 occupations, found {len(df)}")

    field_counts = df["field"].value_counts().sort_index()

    if not all(field_counts == 15):
        raise ValueError(f"Expected 15 occupations per field:\n{field_counts}")

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Created occupations_fields_v3:")
    print(OUTPUT_PATH)
    print("\nField counts:")
    print(field_counts)
    print("\nStereotype label counts:")
    print(df["stereotype_label"].value_counts())


if __name__ == "__main__":
    main()