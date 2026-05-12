import base64
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

hint = 'The shelf has another angle.'
key = 'sp1nef0ld7' # 10 characters, thats the length of the diagonal, prbably shouldnt change it
decoy = 'dustj4cket'
row_hint = 'endpapers1'
flag = 'GIUCTF{sl4nt3dsh3lv3s84}'
rng = random.Random(20260420)

# Build grid
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
n = 10
grid = [[rng.choice(alphabet) for _ in range(n)] for _ in range(n)]
for i, ch in enumerate(row_hint):
    grid[i][0] = ch
for i, ch in enumerate(key):
    grid[i][i] = ch
for i, ch in enumerate(decoy):
    grid[i][n - 1 - i] = ch
rows = ["".join(r) for r in grid]
Path("shelf.txt").write_text(hint + "\n\n" + "\n".join(rows) + "\n", encoding="utf-8")

# Render full flag to block-ASCII, Anti-AI measure, works pretty well
font_path_candidates = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
font = None
for fp in font_path_candidates:
    if os.path.exists(fp):
        font = ImageFont.truetype(fp, 26)
        break
if font is None:
    font = ImageFont.load_default()

dummy = Image.new("L", (10, 10), 255)
d = ImageDraw.Draw(dummy)
bbox = d.textbbox((0, 0), flag, font=font)
w = bbox[2] - bbox[0] + 12
h = bbox[3] - bbox[1] + 12
img = Image.new("L", (w, h), 255)
d = ImageDraw.Draw(img)
d.text((6, 3), flag, font=font, fill=0)
img = img.resize((img.width * 2, img.height * 2))
pix = img.load()

block_lines = []
for y in range(img.height):
    line = []
    for x in range(img.width):
        line.append("█" if pix[x, y] < 180 else " ")
    s = "".join(line).rstrip()
    if "█" in s:
        block_lines.append(s)
banner = "\n".join(block_lines) + "\n"
Path("decrypted_banner.txt").write_text(banner, encoding="utf-8")

cipher = bytes(b ^ key.encode()[i % len(key)] for i, b in enumerate(banner.encode("utf-8")))
Path("cipher.txt").write_text(base64.b64encode(cipher).decode() + "\n", encoding="utf-8")
print("Done.")
