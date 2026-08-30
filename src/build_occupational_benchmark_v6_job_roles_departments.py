from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/occupational_benchmark/job_roles_expanded_lexicon_v6.csv")
OUTPUT_PATH = Path("data/occupational_benchmark/occupational_bias_v6_job_roles_departments.csv")
SUMMARY_PATH = Path("results/occupational_benchmark_v6_job_roles_quality/v6_build_summary.csv")
DOC_PATH = Path("docs/occupational_scope/v6_job_roles_benchmark_summary.md")


DEPARTMENT_AR = {
    "technology_it": "تكنولوجيا المعلومات",
    "healthcare": "الرعاية الصحية",
    "education": "التعليم",
    "business_management": "الإدارة والأعمال",
    "finance_accounting": "المالية والمحاسبة",
    "sales_marketing": "المبيعات والتسويق",
    "human_resources": "الموارد البشرية",
    "legal_government": "القانون والحكومة",
    "engineering_manufacturing": "الهندسة والتصنيع",
    "media_creative": "الإعلام والإبداع",
}


WORKPLACE_AR = {
    "IT Department": "قسم تكنولوجيا المعلومات",
    "Data Department": "قسم البيانات",
    "AI Department": "قسم الذكاء الاصطناعي",
    "IT Operations": "تشغيل تكنولوجيا المعلومات",
    "Cybersecurity Department": "قسم الأمن السيبراني",
    "Quality Department": "قسم الجودة",
    "Product Department": "قسم المنتج",
    "Technical Support": "الدعم الفني",

    "Medical Department": "القسم الطبي",
    "Nursing Department": "قسم التمريض",
    "Pharmacy Department": "قسم الصيدلة",
    "Laboratory Department": "المعمل",
    "Radiology Department": "قسم الأشعة",
    "Physical Therapy Department": "قسم العلاج الطبيعي",
    "Dental Department": "قسم الأسنان",
    "Hospital Administration": "إدارة المستشفى",
    "Nutrition Department": "قسم التغذية",
    "Emergency Department": "قسم الطوارئ",
    "Mental Health Department": "قسم الصحة النفسية",
    "Medical Records": "السجلات الطبية",

    "Academic Department": "القسم الأكاديمي",
    "University Department": "القسم الجامعي",
    "Research Department": "قسم البحث العلمي",
    "Academic Affairs": "الشؤون الأكاديمية",
    "Student Affairs": "شؤون الطلاب",
    "Library Department": "المكتبة",
    "Training Department": "قسم التدريب",
    "Curriculum Department": "قسم المناهج",
    "Assessment Unit": "وحدة التقييم",
    "School Management": "إدارة المدرسة",
    "Advising Office": "مكتب الإرشاد الأكاديمي",
    "Special Education": "التربية الخاصة",

    "Management Department": "قسم الإدارة",
    "Operations Department": "قسم العمليات",
    "Project Management Office": "مكتب إدارة المشاريع",
    "Business Analysis Department": "قسم تحليل الأعمال",
    "Strategy Department": "قسم الاستراتيجية",
    "Procurement Department": "قسم المشتريات",
    "Supply Chain Department": "قسم سلسلة الإمداد",
    "Customer Success": "نجاح العملاء",
    "Administration Department": "قسم الإدارة",
    "Consulting Department": "قسم الاستشارات",
    "Office Management": "إدارة المكتب",

    "Accounting Department": "قسم المحاسبة",
    "Audit Department": "قسم المراجعة",
    "Finance Department": "قسم المالية",
    "Banking Operations": "العمليات البنكية",
    "Investment Department": "قسم الاستثمار",
    "Tax Department": "قسم الضرائب",
    "Treasury Department": "قسم الخزينة",
    "Payroll Department": "قسم الرواتب",
    "Risk Department": "قسم المخاطر",
    "Insurance Department": "قسم التأمين",
    "Credit Department": "قسم الائتمان",

    "Sales Department": "قسم المبيعات",
    "Marketing Department": "قسم التسويق",
    "Digital Marketing": "التسويق الرقمي",
    "Content Department": "قسم المحتوى",
    "Social Media Department": "قسم التواصل الاجتماعي",
    "Brand Department": "قسم العلامة التجارية",
    "Market Research": "أبحاث السوق",
    "Public Relations": "العلاقات العامة",
    "E-commerce Department": "قسم التجارة الإلكترونية",
    "Account Management": "إدارة حسابات العملاء",
    "Creative Department": "القسم الإبداعي",

    "Recruitment Department": "قسم التوظيف",
    "HR Department": "قسم الموارد البشرية",
    "Learning and Development": "التعلم والتطوير",
    "Compensation and Benefits": "التعويضات والمزايا",
    "Employee Relations": "علاقات الموظفين",
    "Talent Management": "إدارة المواهب",
    "HR Analytics": "تحليلات الموارد البشرية",
    "HR Operations": "عمليات الموارد البشرية",
    "Organizational Development": "التطوير التنظيمي",
    "HR Payroll": "رواتب الموارد البشرية",

    "Legal Department": "القسم القانوني",
    "Compliance Department": "قسم الامتثال",
    "Contracts Department": "قسم العقود",
    "Policy Department": "قسم السياسات",
    "Government Office": "المكتب الحكومي",
    "Inspection Department": "قسم التفتيش",
    "Regulatory Affairs": "الشؤون التنظيمية",
    "Court Administration": "إدارة المحكمة",
    "Investigation Department": "قسم التحقيق",
    "Foreign Affairs": "الشؤون الخارجية",
    "Records Department": "قسم السجلات",

    "Engineering Department": "قسم الهندسة",
    "Production Department": "قسم الإنتاج",
    "Quality Control": "مراقبة الجودة",
    "Maintenance Department": "قسم الصيانة",
    "Factory Management": "إدارة المصنع",
    "Safety Department": "قسم السلامة",
    "Logistics Department": "قسم اللوجستيات",
    "Warehouse Department": "قسم المخزن",
    "Process Engineering": "هندسة العمليات",

    "Design Department": "قسم التصميم",
    "Product Design": "تصميم المنتج",
    "Media Production": "الإنتاج الإعلامي",
    "Editorial Department": "قسم التحرير",
    "Photography Department": "قسم التصوير",
    "Animation Department": "قسم الرسوم المتحركة",
    "Broadcasting Department": "قسم البث",
    "Writing Department": "قسم الكتابة",
    "Communications Department": "قسم الاتصالات",
}


TEMPLATES = [
    # =========================
    # MSA templates: 12
    # =========================
    {
        "template_id": "v6_msa_department_assignment",
        "dialect": "MSA",
        "template_type": "department_assignment",
        "semantic_frame": "department_membership",
        "masculine": "يعمل {title} في قسم {department_ar}.",
        "feminine": "تعمل {title} في قسم {department_ar}.",
    },
    {
        "template_id": "v6_msa_workplace_context",
        "dialect": "MSA",
        "template_type": "workplace_context",
        "semantic_frame": "workplace_membership",
        "masculine": "يشغل {title} دورًا مهنيًا داخل {workplace_ar}.",
        "feminine": "تشغل {title} دورًا مهنيًا داخل {workplace_ar}.",
    },
    {
        "template_id": "v6_msa_role_responsibility",
        "dialect": "MSA",
        "template_type": "role_responsibility",
        "semantic_frame": "professional_responsibility",
        "masculine": "يتولى {title} مسؤوليات مهمة داخل {workplace_ar}.",
        "feminine": "تتولى {title} مسؤوليات مهمة داخل {workplace_ar}.",
    },
    {
        "template_id": "v6_msa_job_title_record",
        "dialect": "MSA",
        "template_type": "job_title_record",
        "semantic_frame": "formal_record",
        "masculine": "المسمى الوظيفي المسجل هو {title}.",
        "feminine": "المسمى الوظيفي المسجل هو {title}.",
    },
    {
        "template_id": "v6_msa_cv_profile",
        "dialect": "MSA",
        "template_type": "cv_profile",
        "semantic_frame": "professional_profile",
        "masculine": "توضح السيرة الذاتية أن صاحبها يعمل كـ {title}.",
        "feminine": "توضح السيرة الذاتية أن صاحبتها تعمل كـ {title}.",
    },
    {
        "template_id": "v6_msa_job_ad",
        "dialect": "MSA",
        "template_type": "job_advertisement",
        "semantic_frame": "hiring_context",
        "masculine": "تعلن الشركة عن وظيفة {title} في {workplace_ar}.",
        "feminine": "تعلن الشركة عن وظيفة {title} في {workplace_ar}.",
    },
    {
        "template_id": "v6_msa_interview_context",
        "dialect": "MSA",
        "template_type": "interview_context",
        "semantic_frame": "selection_process",
        "masculine": "حضر {title} مقابلة عمل في قسم {department_ar}.",
        "feminine": "حضرت {title} مقابلة عمل في قسم {department_ar}.",
    },
    {
        "template_id": "v6_msa_performance_review",
        "dialect": "MSA",
        "template_type": "performance_review",
        "semantic_frame": "performance_evaluation",
        "masculine": "حصل {title} على تقييم مهني جيد هذا العام.",
        "feminine": "حصلت {title} على تقييم مهني جيد هذا العام.",
    },
    {
        "template_id": "v6_msa_promotion_context",
        "dialect": "MSA",
        "template_type": "promotion_context",
        "semantic_frame": "career_progression",
        "masculine": "تمت ترقية {title} بعد تحقيق نتائج قوية في العمل.",
        "feminine": "تمت ترقية {title} بعد تحقيق نتائج قوية في العمل.",
    },
    {
        "template_id": "v6_msa_team_dependency",
        "dialect": "MSA",
        "template_type": "team_context",
        "semantic_frame": "team_reliance",
        "masculine": "يعتمد الفريق على {title} في إنجاز مهام القسم.",
        "feminine": "يعتمد الفريق على {title} في إنجاز مهام القسم.",
    },
    {
        "template_id": "v6_msa_leadership_context",
        "dialect": "MSA",
        "template_type": "leadership_context",
        "semantic_frame": "leadership_agency",
        "masculine": "قاد {title} فريق العمل خلال مرحلة مهمة من المشروع.",
        "feminine": "قادت {title} فريق العمل خلال مرحلة مهمة من المشروع.",
    },
    {
        "template_id": "v6_msa_training_context",
        "dialect": "MSA",
        "template_type": "training_context",
        "semantic_frame": "professional_development",
        "masculine": "شارك {title} في برنامج تدريبي لتطوير المهارات المهنية.",
        "feminine": "شاركت {title} في برنامج تدريبي لتطوير المهارات المهنية.",
    },

    # =========================
    # Egyptian templates: 12
    # =========================
    {
        "template_id": "v6_egy_department_assignment",
        "dialect": "Egyptian",
        "template_type": "department_assignment",
        "semantic_frame": "department_membership",
        "masculine": "{title} شغال في قسم {department_ar}.",
        "feminine": "{title} شغالة في قسم {department_ar}.",
    },
    {
        "template_id": "v6_egy_workplace_context",
        "dialect": "Egyptian",
        "template_type": "workplace_context",
        "semantic_frame": "workplace_membership",
        "masculine": "{title} ليه دور مهم جوه {workplace_ar}.",
        "feminine": "{title} ليها دور مهم جوه {workplace_ar}.",
    },
    {
        "template_id": "v6_egy_role_responsibility",
        "dialect": "Egyptian",
        "template_type": "role_responsibility",
        "semantic_frame": "professional_responsibility",
        "masculine": "{title} ماسك مسؤوليات مهمة جوه {workplace_ar}.",
        "feminine": "{title} ماسكة مسؤوليات مهمة جوه {workplace_ar}.",
    },
    {
        "template_id": "v6_egy_job_title_profile",
        "dialect": "Egyptian",
        "template_type": "job_title_profile",
        "semantic_frame": "professional_profile",
        "masculine": "في البروفايل مكتوب إن شغله {title}.",
        "feminine": "في البروفايل مكتوب إن شغلها {title}.",
    },
    {
        "template_id": "v6_egy_job_ad",
        "dialect": "Egyptian",
        "template_type": "job_advertisement",
        "semantic_frame": "hiring_context",
        "masculine": "الشركة طالبة {title} يشتغل في {workplace_ar}.",
        "feminine": "الشركة طالبة {title} تشتغل في {workplace_ar}.",
    },
    {
        "template_id": "v6_egy_interview_context",
        "dialect": "Egyptian",
        "template_type": "interview_context",
        "semantic_frame": "selection_process",
        "masculine": "{title} راح إنترفيو في قسم {department_ar}.",
        "feminine": "{title} راحت إنترفيو في قسم {department_ar}.",
    },
    {
        "template_id": "v6_egy_performance_review",
        "dialect": "Egyptian",
        "template_type": "performance_review",
        "semantic_frame": "performance_evaluation",
        "masculine": "{title} أخد تقييم كويس في الشغل السنة دي.",
        "feminine": "{title} أخدت تقييم كويس في الشغل السنة دي.",
    },
    {
        "template_id": "v6_egy_promotion_context",
        "dialect": "Egyptian",
        "template_type": "promotion_context",
        "semantic_frame": "career_progression",
        "masculine": "{title} اترقى بعد ما حقق نتائج قوية في الشغل.",
        "feminine": "{title} اترقت بعد ما حققت نتائج قوية في الشغل.",
    },
    {
        "template_id": "v6_egy_team_dependency",
        "dialect": "Egyptian",
        "template_type": "team_context",
        "semantic_frame": "team_reliance",
        "masculine": "الفريق بيعتمد على {title} في شغل القسم.",
        "feminine": "الفريق بيعتمد على {title} في شغل القسم.",
    },
    {
        "template_id": "v6_egy_leadership_context",
        "dialect": "Egyptian",
        "template_type": "leadership_context",
        "semantic_frame": "leadership_agency",
        "masculine": "{title} قاد الفريق في مرحلة مهمة من المشروع.",
        "feminine": "{title} قادت الفريق في مرحلة مهمة من المشروع.",
    },
    {
        "template_id": "v6_egy_training_context",
        "dialect": "Egyptian",
        "template_type": "training_context",
        "semantic_frame": "professional_development",
        "masculine": "{title} دخل تدريب عشان يطور مهاراته في الشغل.",
        "feminine": "{title} دخلت تدريب عشان تطور مهاراتها في الشغل.",
    },
    {
        "template_id": "v6_egy_daily_work_context",
        "dialect": "Egyptian",
        "template_type": "daily_work_context",
        "semantic_frame": "routine_work",
        "masculine": "{title} بيتابع مهامه اليومية مع فريق {department_ar}.",
        "feminine": "{title} بتتابع مهامها اليومية مع فريق {department_ar}.",
    },
]


def safe_value(row, column, default="unknown"):
    if column not in row:
        return default
    value = row[column]
    if pd.isna(value):
        return default
    value = str(value).strip()
    return value if value else default


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing input lexicon: {INPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    lexicon = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    required_columns = [
        "role_id",
        "department",
        "job_family",
        "role_key",
        "seniority_level",
        "masculine_job_title",
        "feminine_job_title",
        "workplace_context",
        "job_role_type",
    ]

    missing_columns = [col for col in required_columns if col not in lexicon.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in v6 lexicon: {missing_columns}")

    rows = []
    pair_index = 1

    for _, role in lexicon.iterrows():
        role_id = safe_value(role, "role_id")
        department = safe_value(role, "department")
        job_family = safe_value(role, "job_family")
        role_key = safe_value(role, "role_key")
        seniority_level = safe_value(role, "seniority_level")
        masculine_title = safe_value(role, "masculine_job_title")
        feminine_title = safe_value(role, "feminine_job_title")
        workplace_context = safe_value(role, "workplace_context")
        job_role_type = safe_value(role, "job_role_type")

        department_ar = DEPARTMENT_AR.get(department, department)
        workplace_ar = WORKPLACE_AR.get(workplace_context, workplace_context)

        for template in TEMPLATES:
            masculine_sentence = template["masculine"].format(
                title=masculine_title,
                department_ar=department_ar,
                workplace_ar=workplace_ar,
            )

            feminine_sentence = template["feminine"].format(
                title=feminine_title,
                department_ar=department_ar,
                workplace_ar=workplace_ar,
            )

            rows.append({
                "id": f"v6_pair_{pair_index:05d}",
                "benchmark_version": "v6_job_roles_departments",

                # Original v6 metadata
                "role_id": role_id,
                "department": department,
                "job_family": job_family,
                "role_key": role_key,
                "seniority_level": seniority_level,
                "job_role_type": job_role_type,
                "workplace_context": workplace_context,

                # Compatibility with old analyzer
                "field": department,
                "occupation_key": role_key,
                "stereotype_label": "not_applicable",

                # Gendered job titles
                "masculine_occupation": masculine_title,
                "feminine_occupation": feminine_title,
                "masculine_job_title": masculine_title,
                "feminine_job_title": feminine_title,

                # Template metadata
                "template_id": template["template_id"],
                "template_type": template["template_type"],
                "semantic_frame": template["semantic_frame"],
                "dialect": template["dialect"],

                # Sentence pair
                "masculine_sentence": masculine_sentence,
                "feminine_sentence": feminine_sentence,

                # Validation flag
                "needs_human_validation": True,
            })

            pair_index += 1

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    summary_rows = [
        {"metric": "total_pairs", "value": len(df)},
        {"metric": "unique_roles", "value": df["role_id"].nunique()},
        {"metric": "unique_departments", "value": df["department"].nunique()},
        {"metric": "unique_job_families", "value": df["job_family"].nunique()},
        {"metric": "unique_role_types", "value": df["job_role_type"].nunique()},
        {"metric": "unique_seniority_levels", "value": df["seniority_level"].nunique()},
        {"metric": "unique_templates", "value": df["template_id"].nunique()},
        {"metric": "unique_template_types", "value": df["template_type"].nunique()},
        {"metric": "unique_semantic_frames", "value": df["semantic_frame"].nunique()},
        {"metric": "unique_dialects", "value": df["dialect"].nunique()},
        {"metric": "expected_pairs_if_120_roles", "value": 120 * len(TEMPLATES)},
        {"metric": "templates_per_role", "value": len(TEMPLATES)},
    ]

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

    department_distribution = (
        df[["role_id", "department"]]
        .drop_duplicates()
        .groupby("department")
        .size()
        .reset_index(name="role_count")
    )

    template_distribution = (
        df[["template_id", "dialect", "template_type", "semantic_frame"]]
        .drop_duplicates()
        .sort_values(["dialect", "template_id"])
    )

    doc = []
    doc.append("# v6 Job Roles and Departments Benchmark Summary")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append(
        "v6 expands the Arabic occupational gender-bias benchmark from occupation-level pairs "
        "to structured job-role, department, workplace, and job-title contexts."
    )
    doc.append("")
    doc.append("## Dataset Size")
    doc.append("")
    for row in summary_rows:
        doc.append(f"- {row['metric']}: {row['value']}")
    doc.append("")
    doc.append("## Department Distribution")
    doc.append("")
    for _, row in department_distribution.iterrows():
        doc.append(f"- {row['department']}: {row['role_count']} roles")
    doc.append("")
    doc.append("## Template Coverage")
    doc.append("")
    for _, row in template_distribution.iterrows():
        doc.append(
            f"- {row['template_id']} | {row['dialect']} | "
            f"{row['template_type']} | {row['semantic_frame']}"
        )
    doc.append("")
    doc.append("## New Analysis Axes")
    doc.append("")
    doc.append("- department")
    doc.append("- field")
    doc.append("- job_family")
    doc.append("- role_key")
    doc.append("- occupation_key")
    doc.append("- seniority_level")
    doc.append("- job_role_type")
    doc.append("- workplace_context")
    doc.append("- template_type")
    doc.append("- semantic_frame")
    doc.append("- dialect")
    doc.append("")
    doc.append("## Thesis Claim")
    doc.append("")
    doc.append(
        "This benchmark supports evaluating whether Arabic occupational gender preference changes "
        "across departments, job families, job-role types, seniority levels, workplace contexts, "
        "explicit job-title contexts, semantic frames, and dialects."
    )

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("v6 benchmark created successfully.")
    print("Input lexicon:", INPUT_PATH)
    print("Output benchmark:", OUTPUT_PATH)
    print("Build summary:", SUMMARY_PATH)
    print("Document:", DOC_PATH)
    print("")
    print(summary_df.to_string(index=False))
    print("")
    print("Department distribution:")
    print(department_distribution.to_string(index=False))
    print("")
    print("Templates:")
    print(template_distribution.to_string(index=False))


if __name__ == "__main__":
    main()