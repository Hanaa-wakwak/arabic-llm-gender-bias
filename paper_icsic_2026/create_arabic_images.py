from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

out_dir = Path("paper_icsic_2026/arabic_images")
out_dir.mkdir(parents=True, exist_ok=True)

# Try common Windows Arabic-supporting fonts
font_candidates = [
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\tahoma.ttf",
    r"C:\Windows\Fonts\trado.ttf",
    r"C:\Windows\Fonts\times.ttf",
]

font_path = None
for p in font_candidates:
    if Path(p).exists():
        font_path = p
        break

if font_path is None:
    raise FileNotFoundError("No suitable Windows font found. Try installing Arial or Tahoma.")

font = ImageFont.truetype(font_path, 42)

items = {
    "arabic_masculine_sentence.png": "هذا الطبيب يعمل في المستشفى.",
    "arabic_feminine_sentence.png": "هذه الطبيبة تعمل في المستشفى.",
    "arabic_altabib.png": "الطبيب",
    "arabic_altabiba.png": "الطبيبة",
    "arabic_hatha.png": "هذا",
    "arabic_hathihi.png": "هذه",
}

for filename, text in items.items():
    # Large canvas, right aligned
    img = Image.new("RGB", (900, 130), "white")
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = 860 - text_w
    y = 40 - bbox[1]

    draw.text((x, y), text, fill="black", font=font)

    # Crop whitespace
    bbox2 = img.getbbox()
    cropped = img.crop(bbox2)

    # More precise crop based on non-white pixels
    gray = cropped.convert("L")
    mask = gray.point(lambda p: 255 if p < 250 else 0)
    real_bbox = mask.getbbox()
    if real_bbox:
        cropped = cropped.crop(real_bbox)

    final = Image.new("RGB", (cropped.width + 20, cropped.height + 20), "white")
    final.paste(cropped, (10, 10))
    final.save(out_dir / filename, dpi=(300, 300))

print("Arabic images created in:", out_dir)
for f in out_dir.glob("*.png"):
    print(f)
