# Occupational Benchmark Expansion Plan

## Goal

The current occupational benchmark v1 contains:

* 36 occupations,
* 6 occupational fields,
* 6 occupations per field,
* 144 masculine/feminine sentence pairs.

The goal of the next benchmark version is to expand the occupation coverage while preserving the same controlled counterfactual design.

## Current Version

Current benchmark:

`occupational_bias_v1.csv`

Current size:

| Component                | Count |
| ------------------------ | ----: |
| Fields                   |     6 |
| Occupations per field    |     6 |
| Total occupations        |    36 |
| Templates per occupation |     4 |
| Sentence pairs           |   144 |

## Proposed Expanded Version

The proposed next version is:

`occupational_bias_v2.csv`

Proposed size:

| Component                | Count |
| ------------------------ | ----: |
| Fields                   |     6 |
| Occupations per field    |    10 |
| Total occupations        |    60 |
| Templates per occupation |     4 |
| Sentence pairs           |   240 |

## Why Expand?

The current benchmark is a strong controlled pilot, but expansion is useful for:

1. improving coverage of job-role stereotypes,
2. reducing sensitivity to individual occupation choices,
3. strengthening field-level conclusions,
4. making the benchmark more suitable for thesis and publication use,
5. supporting stronger statistical analysis.

## Fields to Preserve

The same six professional fields will be preserved:

1. STEM
2. Healthcare
3. Education
4. Business
5. Legal/Government
6. Media/Creative

Keeping the same fields allows direct comparison between v1 and v2.

## Expansion Rule

Each field should be expanded from 6 occupations to 10 occupations.

Each new occupation must have:

* masculine Arabic form,
* feminine Arabic form,
* workplace/context,
* stereotype direction,
* field label.

## Quality Criteria

Each occupation should satisfy the following criteria:

1. The masculine and feminine forms must both be common and grammatically valid.
2. The occupation should clearly belong to one professional field.
3. The occupation should support natural MSA and Egyptian sentence templates.
4. The feminine form should not sound rare or artificial.
5. The job should be socially meaningful for gender-bias analysis.

## Proposed Additional Occupations

### STEM

Current: engineer, programmer, data scientist, AI researcher, network engineer, cybersecurity expert.

Add:

1. مهندس برمجيات / مهندسة برمجيات
2. محلل نظم / محللة نظم
3. مطور تطبيقات / مطورة تطبيقات
4. فني صيانة / فنية صيانة

### Healthcare

Current: doctor, nurse, pharmacist, dentist, surgeon, therapist.

Add:

1. أخصائي أشعة / أخصائية أشعة
2. أخصائي تغذية / أخصائية تغذية
3. طبيب أطفال / طبيبة أطفال
4. مسعف / مسعفة

### Education

Current: teacher, professor, researcher, lecturer, school principal, trainer.

Add:

1. مشرف تربوي / مشرفة تربوية
2. أخصائي تعليم / أخصائية تعليم
3. مدرس لغة / مدرسة لغة
4. أمين مكتبة / أمينة مكتبة

### Business

Current: manager, project manager, accountant, HR specialist, business analyst, CEO.

Add:

1. مسؤول مبيعات / مسؤولة مبيعات
2. مستشار أعمال / مستشارة أعمال
3. مدير تسويق / مديرة تسويق
4. رائد أعمال / رائدة أعمال

### Legal/Government

Current: lawyer, judge, police officer, military officer, diplomat, government official.

Add:

1. وكيل نيابة / وكيلة نيابة
2. مستشار قانوني / مستشارة قانونية
3. موظف حكومي / موظفة حكومية
4. مفتش / مفتشة

### Media/Creative

Current: journalist, writer, designer, photographer, artist, content creator.

Add:

1. مخرج / مخرجة
2. محرر / محررة
3. مقدم برامج / مقدمة برامج
4. منتج إعلامي / منتجة إعلامية

## Expected v2 Size

After adding 4 occupations to each field:

* 6 fields,
* 10 occupations per field,
* 60 occupations,
* 4 templates,
* 240 sentence pairs.

## Validation Before Scoring

Before scoring v2, the new occupations should be checked for:

1. Arabic grammatical correctness,
2. natural feminine forms,
3. workplace/context appropriateness,
4. field-label correctness,
5. template compatibility.

## Planned Pipeline

1. Create expanded occupation lexicon:
   `occupations_fields_v2.csv`

2. Generate expanded benchmark:
   `occupational_bias_v2.csv`

3. Run quality checks.

4. Send to human validation.

5. Score the same four models.

6. Compare v1 and v2 results.

7. Decide whether v2 becomes the final thesis benchmark.

## Decision Rule

v2 should replace v1 only if:

1. sentence quality remains high after validation,
2. results remain interpretable,
3. field-level patterns are stable,
4. model-family differences remain statistically significant.

If v2 introduces too much noise, v1 will remain the primary controlled benchmark and v2 will be reported as an expanded ablation.
