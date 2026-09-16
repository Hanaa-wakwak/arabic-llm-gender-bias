from pathlib import Path
import re

tex_path = Path("paper_icsic_2026/ICSIC_2026_IEEE_paper.tex")

if not tex_path.exists():
    raise FileNotFoundError(f"File not found: {tex_path}")

text = tex_path.read_text(encoding="utf-8")

# Backup original file
backup_path = tex_path.with_suffix(".tex.backup_before_arabic_fix")
backup_path.write_text(text, encoding="utf-8")

# 1. Replace Arabic package/font setup with safer Windows-compatible setup
old_block_pattern = re.compile(
    r"\\usepackage\{fontspec\}\s*"
    r"\\usepackage\{polyglossia\}\s*"
    r"\\setmainlanguage\{english\}\s*"
    r"\\setotherlanguage\{arabic\}\s*"
    r"\\newfontfamily\\arabicfont(?:\[[^\]]*\])?\{[^}]+\}",
    re.MULTILINE
)

new_block = r"""
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{arabic}

% Arabic rendering fix for XeLaTeX.
% Tries common Windows Arabic fonts first.
\IfFontExistsTF{Arial}{
  \newfontfamily\arabicfont[Script=Arabic,Language=Arabic,Scale=1.15]{Arial}
}{
  \IfFontExistsTF{Traditional Arabic}{
    \newfontfamily\arabicfont[Script=Arabic,Language=Arabic,Scale=1.15]{Traditional Arabic}
  }{
    \newfontfamily\arabicfont[Script=Arabic,Language=Arabic,Scale=1.15]{Amiri}
  }
}

\newcommand{\ar}[1]{\textarabic{#1}}
""".strip()

if old_block_pattern.search(text):
    text = old_block_pattern.sub(new_block, text)
else:
    # Insert before \def\BibTeX if old block was not found
    marker = r"\def\BibTeX"
    if marker in text:
        text = text.replace(marker, new_block + "\n\n" + marker)
    else:
        raise RuntimeError("Could not find place to insert Arabic font setup.")

# 2. Replace all \textarabic{...} with \ar{...}
text = re.sub(r"\\textarabic\{([^{}]*)\}", r"\\ar{\1}", text)

# 3. Fix common Arabic examples explicitly
replacements = {
    r"\ar{هذا الطبيب يعمل في المستشفى}": r"\ar{هذا الطبيب يعمل في المستشفى.}",
    r"\ar{هذه الطبيبة تعمل في المستشفى}": r"\ar{هذه الطبيبة تعمل في المستشفى.}",
}

for old, new in replacements.items():
    text = text.replace(old, new)

# 4. Save patched tex
tex_path.write_text(text, encoding="utf-8")

print("Arabic rendering patch applied.")
print(f"Backup saved to: {backup_path}")
print(f"Updated file: {tex_path}")
