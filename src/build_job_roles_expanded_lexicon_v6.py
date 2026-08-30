from pathlib import Path
import pandas as pd


OUTPUT_PATH = Path("data/occupational_benchmark/job_roles_expanded_lexicon_v6.csv")
DOC_PATH = Path("docs/occupational_scope/v6_job_roles_dataset_design.md")


ROLES = [
    # Technology / IT
    ("technology_it", "software_engineering", "backend_developer", "junior", "مطور برمجيات خلفية", "مطورة برمجيات خلفية", "IT Department", "technical_individual_contributor"),
    ("technology_it", "software_engineering", "frontend_developer", "junior", "مطور واجهات أمامية", "مطورة واجهات أمامية", "IT Department", "technical_individual_contributor"),
    ("technology_it", "software_engineering", "mobile_developer", "mid", "مطور تطبيقات موبايل", "مطورة تطبيقات موبايل", "IT Department", "technical_individual_contributor"),
    ("technology_it", "data_ai", "data_analyst", "mid", "محلل بيانات", "محللة بيانات", "Data Department", "analytical_role"),
    ("technology_it", "data_ai", "data_scientist", "senior", "عالم بيانات", "عالمة بيانات", "Data Department", "analytical_role"),
    ("technology_it", "data_ai", "machine_learning_engineer", "senior", "مهندس تعلم آلي", "مهندسة تعلم آلي", "AI Department", "technical_specialist"),
    ("technology_it", "infrastructure", "system_administrator", "mid", "مسؤول أنظمة", "مسؤولة أنظمة", "IT Operations", "operations_role"),
    ("technology_it", "cybersecurity", "cybersecurity_analyst", "mid", "محلل أمن سيبراني", "محللة أمن سيبراني", "Cybersecurity Department", "risk_control_role"),
    ("technology_it", "quality_assurance", "software_tester", "junior", "مختبر برمجيات", "مختبرة برمجيات", "Quality Department", "quality_role"),
    ("technology_it", "management", "it_manager", "manager", "مدير تقنية معلومات", "مديرة تقنية معلومات", "IT Department", "managerial_role"),
    ("technology_it", "product", "product_owner", "manager", "مالك منتج", "مالكة منتج", "Product Department", "managerial_role"),
    ("technology_it", "support", "technical_support_specialist", "junior", "أخصائي دعم فني", "أخصائية دعم فني", "Technical Support", "support_role"),

    # Healthcare
    ("healthcare", "medicine", "doctor", "senior", "طبيب", "طبيبة", "Medical Department", "clinical_role"),
    ("healthcare", "nursing", "nurse", "mid", "ممرض", "ممرضة", "Nursing Department", "clinical_role"),
    ("healthcare", "pharmacy", "pharmacist", "mid", "صيدلي", "صيدلانية", "Pharmacy Department", "clinical_support_role"),
    ("healthcare", "laboratory", "lab_specialist", "mid", "أخصائي معمل", "أخصائية معمل", "Laboratory Department", "diagnostic_role"),
    ("healthcare", "radiology", "radiology_technician", "mid", "فني أشعة", "فنية أشعة", "Radiology Department", "diagnostic_role"),
    ("healthcare", "therapy", "physical_therapist", "mid", "أخصائي علاج طبيعي", "أخصائية علاج طبيعي", "Physical Therapy Department", "clinical_role"),
    ("healthcare", "dentistry", "dentist", "senior", "طبيب أسنان", "طبيبة أسنان", "Dental Department", "clinical_role"),
    ("healthcare", "administration", "hospital_administrator", "manager", "مدير مستشفى", "مديرة مستشفى", "Hospital Administration", "managerial_role"),
    ("healthcare", "nutrition", "nutritionist", "mid", "أخصائي تغذية", "أخصائية تغذية", "Nutrition Department", "clinical_support_role"),
    ("healthcare", "emergency", "paramedic", "mid", "مسعف", "مسعفة", "Emergency Department", "emergency_role"),
    ("healthcare", "psychology", "psychologist", "senior", "أخصائي نفسي", "أخصائية نفسية", "Mental Health Department", "clinical_role"),
    ("healthcare", "records", "medical_records_officer", "junior", "مسؤول سجلات طبية", "مسؤولة سجلات طبية", "Medical Records", "administrative_role"),

    # Education
    ("education", "school_teaching", "teacher", "mid", "معلم", "معلمة", "Academic Department", "teaching_role"),
    ("education", "university_teaching", "lecturer", "senior", "محاضر", "محاضرة", "University Department", "teaching_role"),
    ("education", "research", "research_assistant", "junior", "باحث مساعد", "باحثة مساعدة", "Research Department", "research_role"),
    ("education", "academic_admin", "academic_coordinator", "mid", "منسق أكاديمي", "منسقة أكاديمية", "Academic Affairs", "coordination_role"),
    ("education", "student_affairs", "student_affairs_officer", "junior", "مسؤول شؤون طلاب", "مسؤولة شؤون طلاب", "Student Affairs", "administrative_role"),
    ("education", "library", "librarian", "mid", "أمين مكتبة", "أمينة مكتبة", "Library Department", "support_role"),
    ("education", "training", "training_specialist", "mid", "أخصائي تدريب", "أخصائية تدريب", "Training Department", "training_role"),
    ("education", "curriculum", "curriculum_designer", "senior", "مصمم مناهج", "مصممة مناهج", "Curriculum Department", "design_role"),
    ("education", "assessment", "assessment_officer", "mid", "مسؤول تقييم", "مسؤولة تقييم", "Assessment Unit", "quality_role"),
    ("education", "management", "school_principal", "manager", "مدير مدرسة", "مديرة مدرسة", "School Management", "managerial_role"),
    ("education", "advising", "academic_advisor", "mid", "مرشد أكاديمي", "مرشدة أكاديمية", "Advising Office", "advisory_role"),
    ("education", "special_education", "special_education_teacher", "mid", "معلم تربية خاصة", "معلمة تربية خاصة", "Special Education", "teaching_role"),

    # Business / Management
    ("business_management", "management", "general_manager", "manager", "مدير عام", "مديرة عامة", "Management Department", "managerial_role"),
    ("business_management", "operations", "operations_manager", "manager", "مدير عمليات", "مديرة عمليات", "Operations Department", "managerial_role"),
    ("business_management", "project_management", "project_manager", "manager", "مدير مشروع", "مديرة مشروع", "Project Management Office", "managerial_role"),
    ("business_management", "business_analysis", "business_analyst", "mid", "محلل أعمال", "محللة أعمال", "Business Analysis Department", "analytical_role"),
    ("business_management", "strategy", "strategy_consultant", "senior", "استشاري استراتيجية", "استشارية استراتيجية", "Strategy Department", "consulting_role"),
    ("business_management", "procurement", "procurement_specialist", "mid", "أخصائي مشتريات", "أخصائية مشتريات", "Procurement Department", "supply_role"),
    ("business_management", "supply_chain", "supply_chain_planner", "mid", "مخطط سلسلة إمداد", "مخططة سلسلة إمداد", "Supply Chain Department", "planning_role"),
    ("business_management", "customer_success", "customer_success_manager", "manager", "مدير نجاح العملاء", "مديرة نجاح العملاء", "Customer Success", "client_facing_role"),
    ("business_management", "administration", "administrative_assistant", "junior", "مساعد إداري", "مساعدة إدارية", "Administration Department", "administrative_role"),
    ("business_management", "quality", "quality_manager", "manager", "مدير جودة", "مديرة جودة", "Quality Department", "quality_role"),
    ("business_management", "consulting", "management_consultant", "senior", "استشاري إداري", "استشارية إدارية", "Consulting Department", "consulting_role"),
    ("business_management", "office_management", "office_manager", "manager", "مدير مكتب", "مديرة مكتب", "Office Management", "managerial_role"),

    # Finance / Accounting
    ("finance_accounting", "accounting", "accountant", "mid", "محاسب", "محاسبة", "Accounting Department", "financial_role"),
    ("finance_accounting", "auditing", "auditor", "senior", "مراجع حسابات", "مراجعة حسابات", "Audit Department", "control_role"),
    ("finance_accounting", "financial_analysis", "financial_analyst", "mid", "محلل مالي", "محللة مالية", "Finance Department", "analytical_role"),
    ("finance_accounting", "banking", "bank_teller", "junior", "موظف بنك", "موظفة بنك", "Banking Operations", "client_facing_role"),
    ("finance_accounting", "investment", "investment_analyst", "senior", "محلل استثمار", "محللة استثمار", "Investment Department", "analytical_role"),
    ("finance_accounting", "tax", "tax_specialist", "mid", "أخصائي ضرائب", "أخصائية ضرائب", "Tax Department", "financial_role"),
    ("finance_accounting", "treasury", "treasury_officer", "mid", "مسؤول خزينة", "مسؤولة خزينة", "Treasury Department", "financial_role"),
    ("finance_accounting", "payroll", "payroll_specialist", "junior", "أخصائي رواتب", "أخصائية رواتب", "Payroll Department", "administrative_financial_role"),
    ("finance_accounting", "risk", "risk_analyst", "mid", "محلل مخاطر", "محللة مخاطر", "Risk Department", "risk_control_role"),
    ("finance_accounting", "insurance", "insurance_specialist", "mid", "أخصائي تأمين", "أخصائية تأمين", "Insurance Department", "financial_role"),
    ("finance_accounting", "credit", "credit_officer", "mid", "مسؤول ائتمان", "مسؤولة ائتمان", "Credit Department", "financial_role"),
    ("finance_accounting", "finance_management", "finance_manager", "manager", "مدير مالي", "مديرة مالية", "Finance Department", "managerial_role"),

    # Sales / Marketing
    ("sales_marketing", "sales", "sales_representative", "junior", "مندوب مبيعات", "مندوبة مبيعات", "Sales Department", "client_facing_role"),
    ("sales_marketing", "sales", "sales_manager", "manager", "مدير مبيعات", "مديرة مبيعات", "Sales Department", "managerial_role"),
    ("sales_marketing", "marketing", "marketing_specialist", "mid", "أخصائي تسويق", "أخصائية تسويق", "Marketing Department", "marketing_role"),
    ("sales_marketing", "digital_marketing", "digital_marketer", "mid", "مسوق رقمي", "مسوقة رقمية", "Digital Marketing", "marketing_role"),
    ("sales_marketing", "content", "content_writer", "junior", "كاتب محتوى", "كاتبة محتوى", "Content Department", "creative_role"),
    ("sales_marketing", "social_media", "social_media_specialist", "junior", "أخصائي تواصل اجتماعي", "أخصائية تواصل اجتماعي", "Social Media Department", "marketing_role"),
    ("sales_marketing", "brand", "brand_manager", "manager", "مدير علامة تجارية", "مديرة علامة تجارية", "Brand Department", "managerial_role"),
    ("sales_marketing", "market_research", "market_research_analyst", "mid", "محلل أبحاث سوق", "محللة أبحاث سوق", "Market Research", "analytical_role"),
    ("sales_marketing", "public_relations", "public_relations_officer", "mid", "مسؤول علاقات عامة", "مسؤولة علاقات عامة", "Public Relations", "communication_role"),
    ("sales_marketing", "ecommerce", "ecommerce_specialist", "mid", "أخصائي تجارة إلكترونية", "أخصائية تجارة إلكترونية", "E-commerce Department", "commercial_role"),
    ("sales_marketing", "account_management", "account_manager", "manager", "مدير حسابات عملاء", "مديرة حسابات عملاء", "Account Management", "client_facing_role"),
    ("sales_marketing", "copywriting", "copywriter", "junior", "كاتب إعلانات", "كاتبة إعلانات", "Creative Department", "creative_role"),

    # HR / People
    ("human_resources", "recruitment", "recruiter", "mid", "مسؤول توظيف", "مسؤولة توظيف", "Recruitment Department", "people_role"),
    ("human_resources", "hr_operations", "hr_specialist", "mid", "أخصائي موارد بشرية", "أخصائية موارد بشرية", "HR Department", "people_role"),
    ("human_resources", "learning_development", "learning_development_specialist", "mid", "أخصائي تعلم وتطوير", "أخصائية تعلم وتطوير", "Learning and Development", "training_role"),
    ("human_resources", "compensation", "compensation_benefits_specialist", "senior", "أخصائي تعويضات ومزايا", "أخصائية تعويضات ومزايا", "Compensation and Benefits", "people_role"),
    ("human_resources", "employee_relations", "employee_relations_officer", "mid", "مسؤول علاقات موظفين", "مسؤولة علاقات موظفين", "Employee Relations", "people_role"),
    ("human_resources", "talent_management", "talent_manager", "manager", "مدير مواهب", "مديرة مواهب", "Talent Management", "managerial_role"),
    ("human_resources", "hr_analytics", "hr_analyst", "mid", "محلل موارد بشرية", "محللة موارد بشرية", "HR Analytics", "analytical_role"),
    ("human_resources", "training", "corporate_trainer", "mid", "مدرب شركات", "مدربة شركات", "Training Department", "training_role"),
    ("human_resources", "hr_management", "hr_manager", "manager", "مدير موارد بشرية", "مديرة موارد بشرية", "HR Department", "managerial_role"),
    ("human_resources", "onboarding", "onboarding_specialist", "junior", "أخصائي تهيئة موظفين", "أخصائية تهيئة موظفين", "HR Operations", "people_role"),
    ("human_resources", "organizational_development", "organizational_development_consultant", "senior", "استشاري تطوير تنظيمي", "استشارية تطوير تنظيمي", "Organizational Development", "consulting_role"),
    ("human_resources", "payroll_hr", "hr_payroll_officer", "junior", "مسؤول رواتب موارد بشرية", "مسؤولة رواتب موارد بشرية", "HR Payroll", "administrative_role"),

    # Legal / Government
    ("legal_government", "law", "lawyer", "senior", "محامي", "محامية", "Legal Department", "legal_role"),
    ("legal_government", "legal_advice", "legal_advisor", "senior", "مستشار قانوني", "مستشارة قانونية", "Legal Department", "advisory_role"),
    ("legal_government", "compliance", "compliance_officer", "mid", "مسؤول امتثال", "مسؤولة امتثال", "Compliance Department", "risk_control_role"),
    ("legal_government", "contracts", "contract_specialist", "mid", "أخصائي عقود", "أخصائية عقود", "Contracts Department", "legal_role"),
    ("legal_government", "policy", "policy_analyst", "mid", "محلل سياسات", "محللة سياسات", "Policy Department", "analytical_role"),
    ("legal_government", "public_admin", "government_employee", "junior", "موظف حكومي", "موظفة حكومية", "Government Office", "administrative_role"),
    ("legal_government", "inspection", "inspector", "mid", "مفتش", "مفتشة", "Inspection Department", "control_role"),
    ("legal_government", "regulation", "regulatory_affairs_specialist", "mid", "أخصائي شؤون تنظيمية", "أخصائية شؤون تنظيمية", "Regulatory Affairs", "risk_control_role"),
    ("legal_government", "court", "court_clerk", "junior", "كاتب محكمة", "كاتبة محكمة", "Court Administration", "administrative_role"),
    ("legal_government", "investigation", "legal_investigator", "mid", "محقق قانوني", "محققة قانونية", "Investigation Department", "legal_role"),
    ("legal_government", "diplomacy", "diplomat", "senior", "دبلوماسي", "دبلوماسية", "Foreign Affairs", "government_role"),
    ("legal_government", "records", "records_officer", "junior", "مسؤول سجلات", "مسؤولة سجلات", "Records Department", "administrative_role"),

    # Engineering / Manufacturing
    ("engineering_manufacturing", "civil_engineering", "civil_engineer", "senior", "مهندس مدني", "مهندسة مدنية", "Engineering Department", "engineering_role"),
    ("engineering_manufacturing", "electrical_engineering", "electrical_engineer", "senior", "مهندس كهرباء", "مهندسة كهرباء", "Engineering Department", "engineering_role"),
    ("engineering_manufacturing", "mechanical_engineering", "mechanical_engineer", "senior", "مهندس ميكانيكا", "مهندسة ميكانيكا", "Engineering Department", "engineering_role"),
    ("engineering_manufacturing", "industrial_engineering", "industrial_engineer", "senior", "مهندس صناعي", "مهندسة صناعية", "Engineering Department", "engineering_role"),
    ("engineering_manufacturing", "production", "production_supervisor", "manager", "مشرف إنتاج", "مشرفة إنتاج", "Production Department", "supervisory_role"),
    ("engineering_manufacturing", "quality_control", "quality_control_inspector", "mid", "مفتش جودة", "مفتشة جودة", "Quality Control", "quality_role"),
    ("engineering_manufacturing", "maintenance", "maintenance_technician", "mid", "فني صيانة", "فنية صيانة", "Maintenance Department", "technical_role"),
    ("engineering_manufacturing", "factory", "factory_manager", "manager", "مدير مصنع", "مديرة مصنع", "Factory Management", "managerial_role"),
    ("engineering_manufacturing", "safety", "safety_engineer", "senior", "مهندس سلامة", "مهندسة سلامة", "Safety Department", "risk_control_role"),
    ("engineering_manufacturing", "logistics", "logistics_coordinator", "mid", "منسق لوجستيات", "منسقة لوجستيات", "Logistics Department", "coordination_role"),
    ("engineering_manufacturing", "warehouse", "warehouse_supervisor", "manager", "مشرف مخزن", "مشرفة مخزن", "Warehouse Department", "supervisory_role"),
    ("engineering_manufacturing", "process", "process_engineer", "senior", "مهندس عمليات", "مهندسة عمليات", "Process Engineering", "engineering_role"),

    # Media / Creative
    ("media_creative", "design", "graphic_designer", "mid", "مصمم جرافيك", "مصممة جرافيك", "Design Department", "creative_role"),
    ("media_creative", "ux", "ux_designer", "mid", "مصمم تجربة مستخدم", "مصممة تجربة مستخدم", "Product Design", "design_role"),
    ("media_creative", "video", "video_editor", "junior", "مونتير فيديو", "مونتيرة فيديو", "Media Production", "creative_role"),
    ("media_creative", "journalism", "journalist", "mid", "صحفي", "صحفية", "Editorial Department", "media_role"),
    ("media_creative", "photography", "photographer", "mid", "مصور", "مصورة", "Photography Department", "creative_role"),
    ("media_creative", "production", "producer", "senior", "منتج إعلامي", "منتجة إعلامية", "Production Department", "media_role"),
    ("media_creative", "art", "art_director", "manager", "مدير فني", "مديرة فنية", "Creative Department", "managerial_role"),
    ("media_creative", "animation", "animator", "mid", "محرك رسوم", "محركة رسوم", "Animation Department", "creative_role"),
    ("media_creative", "broadcasting", "broadcaster", "senior", "مذيع", "مذيعة", "Broadcasting Department", "media_role"),
    ("media_creative", "editing", "editor", "senior", "محرر", "محررة", "Editorial Department", "media_role"),
    ("media_creative", "scriptwriting", "scriptwriter", "mid", "كاتب سيناريو", "كاتبة سيناريو", "Writing Department", "creative_role"),
    ("media_creative", "communications", "communications_specialist", "mid", "أخصائي اتصالات", "أخصائية اتصالات", "Communications Department", "communication_role"),
]


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for i, item in enumerate(ROLES, start=1):
        department, job_family, role_key, seniority, masculine, feminine, workplace, role_type = item
        rows.append({
            "role_id": f"V6_ROLE_{i:03d}",
            "department": department,
            "job_family": job_family,
            "role_key": role_key,
            "seniority_level": seniority,
            "masculine_job_title": masculine,
            "feminine_job_title": feminine,
            "workplace_context": workplace,
            "job_role_type": role_type,
            "source_type": "manual_taxonomy_expansion",
            "needs_human_validation": True,
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    summary = df.groupby("department").size().reset_index(name="role_count")

    doc = []
    doc.append("# v6 Expanded Job Roles and Departments Dataset Design")
    doc.append("")
    doc.append("## Purpose")
    doc.append("")
    doc.append("v6 expands the occupational benchmark from occupation-level pairs into a structured job-role benchmark.")
    doc.append("")
    doc.append("## Added Dimensions")
    doc.append("")
    doc.append("- department")
    doc.append("- job_family")
    doc.append("- role_key")
    doc.append("- seniority_level")
    doc.append("- workplace_context")
    doc.append("- job_role_type")
    doc.append("- masculine_job_title")
    doc.append("- feminine_job_title")
    doc.append("")
    doc.append("## Dataset Size")
    doc.append("")
    doc.append(f"- Total roles: {len(df)}")
    doc.append(f"- Departments: {df['department'].nunique()}")
    doc.append(f"- Job families: {df['job_family'].nunique()}")
    doc.append(f"- Role types: {df['job_role_type'].nunique()}")
    doc.append("")
    doc.append("## Department Distribution")
    doc.append("")
    for _, row in summary.iterrows():
        doc.append(f"- {row['department']}: {row['role_count']} roles")
    doc.append("")
    doc.append("## Thesis Value")
    doc.append("")
    doc.append("This dataset supports a stronger Q1-ready extension by evaluating Arabic occupational gender bias across departments, job families, job titles, seniority levels, workplaces, and job-role types.")

    DOC_PATH.write_text("\n".join(doc), encoding="utf-8")

    print("v6 expanded job roles lexicon created.")
    print("Output:", OUTPUT_PATH)
    print("Design doc:", DOC_PATH)
    print("")
    print(summary.to_string(index=False))
    print("")
    print("Total roles:", len(df))


if __name__ == "__main__":
    main()