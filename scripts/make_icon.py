"""Generate .claude-plugin/icon.png (1024x1024). Run: uv run --with pillow scripts/make_icon.py"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
SCALE = 2  # supersample for smooth edges
S = SIZE * SCALE
ROOT = Path(__file__).resolve().parent.parent
FONT = "C:/Windows/Fonts/segoeuib.ttf"


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main():
    # Diagonal gradient background
    top, bottom = (79, 70, 229), (147, 51, 234)  # indigo -> violet
    grad = Image.new("RGB", (S, S))
    px = grad.load()
    for y in range(S):
        for x in range(S):
            px[x, y] = lerp(top, bottom, (x + y) / (2 * S))

    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)

    # Interviewer bubble (big, white) with "?"
    bx0, by0, bx1, by1 = int(S * 0.13), int(S * 0.16), int(S * 0.72), int(S * 0.58)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=int(S * 0.08), fill="white")
    d.polygon([(int(S * 0.24), by1 - 4), (int(S * 0.20), int(S * 0.70)), (int(S * 0.38), by1 - 4)], fill="white")
    qf = ImageFont.truetype(FONT, int(S * 0.30))
    d.text(((bx0 + bx1) // 2, (by0 + by1) // 2 + int(S * 0.005)), "?", font=qf, fill=top, anchor="mm")

    # Candidate bubble (small, green) with check mark
    cx0, cy0, cx1, cy1 = int(S * 0.50), int(S * 0.54), int(S * 0.87), int(S * 0.82)
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=int(S * 0.07), fill=(34, 197, 94), outline="white", width=int(S * 0.018))
    d.polygon([(int(S * 0.76), cy1 - 6), (int(S * 0.81), int(S * 0.90)), (int(S * 0.66), cy1 - 6)], fill=(34, 197, 94))
    w = int(S * 0.035)
    pts = [(int(S * 0.595), int(S * 0.68)), (int(S * 0.655), int(S * 0.74)), (int(S * 0.775), int(S * 0.61))]
    d.line(pts, fill="white", width=w, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - w // 2, p[1] - w // 2, p[0] + w // 2, p[1] + w // 2], fill="white")

    out = ROOT / ".claude-plugin" / "icon.png"
    img.resize((SIZE, SIZE), Image.LANCZOS).save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
