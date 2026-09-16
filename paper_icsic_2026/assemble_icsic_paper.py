from pathlib import Path

paper_dir = Path("paper_icsic_2026")

sections = [
    "00_title_abstract_keywords.md",
    "01_introduction.md",
    "02_related_work.md",
    "03_methodology.md",
    "04_experiments_results.md",
    "05_discussion.md",
    "06_conclusion.md",
    "07_references.md",
]

output_path = paper_dir / "ICSIC_2026_paper_draft.md"

parts = []

for section in sections:
    path = paper_dir / section
    if not path.exists():
        raise FileNotFoundError(f"Missing section file: {path}")
    text = path.read_text(encoding="utf-8")
    parts.append(text.strip())

final_text = "\n\n---\n\n".join(parts)
output_path.write_text(final_text + "\n", encoding="utf-8")

print(f"Assembled paper written to: {output_path}")
print(f"Sections included: {len(sections)}")
print(f"Approximate word count: {len(final_text.split())}")
