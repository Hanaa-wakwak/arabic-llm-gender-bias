from pathlib import Path
import re

tex_path = Path("paper_icsic_2026/ICSIC_2026_IEEE_paper.tex")
text = tex_path.read_text(encoding="utf-8")

backup = tex_path.with_suffix(".tex.backup_image_arabic_fix")
backup.write_text(text, encoding="utf-8")

# Remove risky Arabic packages/macros if present
text = re.sub(r"\\usepackage\{polyglossia\}\s*", "", text)
text = re.sub(r"\\setmainlanguage\{english\}\s*", "", text)
text = re.sub(r"\\setotherlanguage\{arabic\}\s*", "", text)
text = re.sub(r"\\usepackage\{bidi\}\s*", "", text)
text = re.sub(r"\\newfontfamily\\arabicfont[^\n]*\n", "", text)
text = re.sub(r"\\newfontfamily\\arabicfontsf[^\n]*\n", "", text)
text = re.sub(r"\\newfontfamily\\arabicfonttt[^\n]*\n", "", text)
text = re.sub(r"\\newcommand\{\\ar\}\[1\]\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\s*", "", text)

# Remove broken IfFontExistsTF block if previous patch inserted it
text = re.sub(
    r"% Arabic rendering setup for XeLaTeX[\s\S]*?\\newcommand\{\\ar\}\[1\]\{[\s\S]*?\}\s*",
    "",
    text,
    count=1
)

text = re.sub(
    r"% Arabic rendering fix for XeLaTeX\.[\s\S]*?\\newcommand\{\\ar\}\[1\]\{[\s\S]*?\}\s*",
    "",
    text,
    count=1
)

# Add graphic helper macros after packages
marker = r"\def\BibTeX"
image_macros = r"""
% Arabic examples are inserted as images to avoid Arabic font/rendering issues in IEEE PDF.
\newcommand{\arabicmasc}{\raisebox{-0.25em}{\includegraphics[height=1.35em]{arabic_images/arabic_masculine_sentence.png}}}
\newcommand{\arabicfem}{\raisebox{-0.25em}{\includegraphics[height=1.35em]{arabic_images/arabic_feminine_sentence.png}}}
\newcommand{\arabicaltabib}{\raisebox{-0.2em}{\includegraphics[height=1.15em]{arabic_images/arabic_altabib.png}}}
\newcommand{\arabicaltabiba}{\raisebox{-0.2em}{\includegraphics[height=1.15em]{arabic_images/arabic_altabiba.png}}}
\newcommand{\arabichatha}{\raisebox{-0.2em}{\includegraphics[height=1.15em]{arabic_images/arabic_hatha.png}}}
\newcommand{\arabichathihi}{\raisebox{-0.2em}{\includegraphics[height=1.15em]{arabic_images/arabic_hathihi.png}}}
""".strip()

if marker not in text:
    raise RuntimeError("Could not find BibTeX marker.")

if r"\newcommand{\arabicmasc}" not in text:
    text = text.replace(marker, image_macros + "\n\n" + marker, 1)

# Replace Arabic macros/text commands with image macros
replacements = {
    r"\ar{هذا الطبيب يعمل في المستشفى.}": r"\arabicmasc{}",
    r"\ar{هذه الطبيبة تعمل في المستشفى.}": r"\arabicfem{}",
    r"\ar{هذا الطبيب يعمل في المستشفى}": r"\arabicmasc{}",
    r"\ar{هذه الطبيبة تعمل في المستشفى}": r"\arabicfem{}",
    r"\textarabic{هذا الطبيب يعمل في المستشفى.}": r"\arabicmasc{}",
    r"\textarabic{هذه الطبيبة تعمل في المستشفى.}": r"\arabicfem{}",
    r"\textarabic{هذا الطبيب يعمل في المستشفى}": r"\arabicmasc{}",
    r"\textarabic{هذه الطبيبة تعمل في المستشفى}": r"\arabicfem{}",
    r"\ar{الطبيب}": r"\arabicaltabib{}",
    r"\ar{الطبيبة}": r"\arabicaltabiba{}",
    r"\ar{هذا}": r"\arabichatha{}",
    r"\ar{هذه}": r"\arabichathihi{}",
    r"\textarabic{الطبيب}": r"\arabicaltabib{}",
    r"\textarabic{الطبيبة}": r"\arabicaltabiba{}",
    r"\textarabic{هذا}": r"\arabichatha{}",
    r"\textarabic{هذه}": r"\arabichathihi{}",
}

for old, new in replacements.items():
    text = text.replace(old, new)

# If previous PDF lost Arabic examples completely, force the example paragraph
text = re.sub(
    r"For example, the masculine sentence\s*.*?\s*must be paired with the feminine sentence\s*.*?, where both the occupational noun and the demonstrative are adjusted\.",
    r"For example, the masculine sentence \arabicmasc{} must be paired with the feminine sentence \arabicfem{}, where both the occupational noun and the demonstrative are adjusted.",
    text,
    flags=re.DOTALL,
    count=1
)

# Force methodology quote block
text = re.sub(
    r"Masculine:\s*(?:\\arabicmasc\{\}|\\ar\{[^}]*\}|\\textarabic\{[^}]*\})?\s*Feminine:\s*(?:\\arabicfem\{\}|\\ar\{[^}]*\}|\\textarabic\{[^}]*\})?",
    r"Masculine: \arabicmasc{}\n\nFeminine: \arabicfem{}",
    text,
    count=1
)

# Force noun/demonstrative sentence
text = re.sub(
    r"The pair changes the occupational noun from\s*.*?\s*to\s*.*?\s*and the demonstrative from\s*.*?\s*to\s*.*?\.",
    r"The pair changes the occupational noun from \arabicaltabib{} to \arabicaltabiba{} and the demonstrative from \arabichatha{} to \arabichathihi{}.",
    text,
    flags=re.DOTALL,
    count=1
)

tex_path.write_text(text, encoding="utf-8")

print("Patched LaTeX to use Arabic PNG images.")
print("Backup:", backup)
print("Updated:", tex_path)
