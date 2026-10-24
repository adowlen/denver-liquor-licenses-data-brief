"""Composite the headline figure over the generated hero illustration.
Text sits on the clean dark field in the upper third; a soft dark
scrim band is added behind the text for legibility. Lines are wrapped
by measured text width so nothing runs off the frame."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

root = pathlib.Path(__file__).resolve().parent.parent
src = root / "hero_source" / "media-generation-hero-illustration-0-997438a3-5854-4c7e-8a35-567bd7d1d72b.webp"
img = Image.open(src).convert("RGB")
W, H = img.size
scrim = Image.new("RGB", (W, int(H * 0.34)), (16, 20, 23))
img.paste(scrim, (0, 0))
d = ImageDraw.Draw(img)

def font(size, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, size)

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

MAXW = W - 124
d.text((60, 42), "554 of 1,965 licenses", font=font(int(H * 0.100)), fill=(245, 168, 0))
sub_f = font(int(H * 0.037), bold=False)
y = 42 + int(H * 0.128)
for line in wrap("28.2% of Denver's active liquor licenses sit in five neighborhoods - home to 7.4% of its residents.", sub_f, MAXW):
    d.text((62, y), line, font=sub_f, fill=(242, 242, 242))
    y += int(H * 0.052)
src_f = font(int(H * 0.027), bold=False)
for line in wrap("Source: Denver Open Data, liquor license register (2,215 records, pulled Oct 23, 2026); ACS 2024 5-year population", src_f, MAXW):
    d.text((62, y + 6), line, font=src_f, fill=(150, 210, 200))
    y += int(H * 0.040)
img.save(root / "hero.png")
print("hero", img.size)
