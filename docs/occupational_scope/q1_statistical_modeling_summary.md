# Q1 Statistical Modeling and Factor Sensitivity Summary

## Purpose

This analysis strengthens the publication version by comparing gender-preference scores across controlled v6 job-role data and ArabJobs v7 real-world job-ad data.

## Inputs

- v6 expanded job-role scoring outputs
- ArabJobs v7 external real-world job-ad scoring outputs

## Output Files

- Combined scoring file: `results\q1_statistical_modeling\q1_combined_scoring_outputs_v6_arabjobs.csv`
- Overall by dataset and model: `results\q1_statistical_modeling\q1_overall_by_dataset_source_and_model.csv`
- Factor sensitivity summary: `results\q1_statistical_modeling\q1_factor_effect_strength_summary.csv`

## Factor Sensitivity Interpretation

For each factor, the analysis computes the range of average score_difference across factor levels. A larger range indicates that measured gender preference is more sensitive to that factor.

## Strongest Factor Effects

### arabjobs_v7

- job_family: range=0.9744117540471695, strongest feminine=pharmacy, strongest masculine=administration
- job_role_type: range=0.9127973471627091, strongest feminine=clinical_support_role, strongest masculine=administrative_role
- template_type: range=0.5562131926601923, strongest feminine=application_context, strongest masculine=recruitment_context
- semantic_frame: range=0.5562131926601923, strongest feminine=candidate_application, strongest masculine=hiring_language
- field: range=0.5074105260987304, strongest feminine=education, strongest masculine=business_management
- department: range=0.5074105260987304, strongest feminine=education, strongest masculine=business_management
- seniority_level: range=0.3292557859585288, strongest feminine=senior, strongest masculine=junior
- model_name: range=0.019494019754327366, strongest feminine=aubmindlab/aragpt2-base, strongest masculine=bigscience/bloom-560m

### v6_job_roles

- template_type: range=1.247736042737961, strongest feminine=daily_work_context, strongest masculine=job_title_record
- semantic_frame: range=1.247736042737961, strongest feminine=routine_work, strongest masculine=formal_record
- job_family: range=0.8355489571889241, strongest feminine=nursing, strongest masculine=digital_marketing
- job_role_type: range=0.6036098102728525, strongest feminine=technical_specialist, strongest masculine=technical_role
- model_name: range=0.28564757862024837, strongest feminine=aubmindlab/aragpt2-base, strongest masculine=bigscience/bloom-560m
- field: range=0.16296537799967659, strongest feminine=education, strongest masculine=sales_marketing
- department: range=0.16296537799967659, strongest feminine=education, strongest masculine=sales_marketing
- dialect: range=0.14878189435435665, strongest feminine=Egyptian, strongest masculine=MSA

## Publication Claim

This analysis supports the claim that Arabic occupational gender-bias measurement is sensitive to dataset source, model choice, template formulation, dialect, department, job family, seniority, and job-role framing.