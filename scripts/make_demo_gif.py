"""Render docs/demo.gif: a terminal-style animation of a mock-interview exchange.
Run: uv run --with pillow scripts/make_demo_gif.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1000, 560
PAD_X, TOP = 28, 58
FS = 17
LH = 25
FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", FS)
BOLD = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", FS)
TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)

BG, BAR = (24, 24, 37), (40, 40, 58)
FG, DIM = (220, 223, 235), (130, 135, 160)
ACC, GREEN, YEL, CYAN, PINK = (167, 139, 250), (74, 222, 128), (250, 204, 21), (103, 232, 249), (244, 114, 182)

# Each line: list of (text, color, bold). Kind: "type" = typed char by char (user), "out" = printed (Claude)
SCRIPT = [
    ("type", [("> ", ACC, True), ("/mock-interview", FG, False)]),
    ("pause", 500),
    ("out", [("● ", ACC, True), ("Looked at your project: Next.js + Supabase shop with Stripe checkout.", DIM, False)]),
    ("out", [("  Junior Full-stack · Practice mode · 5 questions", DIM, False)]),
    ("out", []),
    ("out", [("Question 3/5 · Project deep-dive", CYAN, True)]),
    ("out", [("In app/api/checkout/route.ts you call Stripe directly. What", FG, False)]),
    ("out", [("happens if Stripe is slow or returns an error?", FG, False)]),
    ("pause", 900),
    ("out", []),
    ("type", [("> ", ACC, True), ("i think it just shows an error to the user", FG, False)]),
    ("pause", 700),
    ("out", []),
    ("out", [("Score: 2/5", YEL, True), (" · You saw the user effect, not the system.", FG, False)]),
    ("out", [("+ Good: ", GREEN, True), ("you thought about the user experience.", FG, False)]),
    ("out", [("! Missing: ", PINK, True), ("no timeout, error isn't logged, and the card", FG, False)]),
    ("out", [("  may be charged while the order is never saved.", FG, False)]),
    ("out", [("» Stronger answer:", ACC, True)]),
    ("out", [("  \"I'd add a timeout, log the error with the order ID and", FG, False)]),
    ("out", [("  show a retry message. Most importantly, Stripe webhooks are", FG, False)]),
    ("out", [("  the source of truth, so a paid order is never lost.\"", FG, False)]),
    ("out", [("Tip: ", YEL, True), ("for 'what if X fails', cover user, data, monitoring.", FG, False)]),
    ("pause", 3500),
]


def base():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 38], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([16 + i * 22, 13, 28 + i * 22, 25], fill=c)
    d.text((W // 2, 19), "claude — mock-interview", font=TITLE, fill=DIM, anchor="mm")
    return img


def draw_line(d, y, segs, upto=None):
    x = PAD_X
    left = upto
    for text, color, bold in segs:
        if left is not None:
            text = text[: max(0, left)]
            left -= len(text) if left >= len(text) else left
        f = BOLD if bold else FONT
        d.text((x, y), text, font=f, fill=color)
        x += d.textlength(text, font=f)
    return x


def main():
    frames, durations = [], []
    lines = []  # finished lines

    def snapshot(partial=None, upto=None, cursor=False, ms=80):
        img = base()
        d = ImageDraw.Draw(img)
        y = TOP
        for segs in lines:
            draw_line(d, y, segs)
            y += LH
        if partial is not None:
            x = draw_line(d, y, partial, upto)
            if cursor:
                d.rectangle([x + 1, y + 3, x + 10, y + FS + 3], fill=FG)
        frames.append(img)
        durations.append(ms)

    for kind, payload in SCRIPT:
        if kind == "pause":
            snapshot(ms=payload)
        elif kind == "out":
            lines.append(payload)
            snapshot(ms=140)
        elif kind == "type":
            total = sum(len(t) for t, _, _ in payload)
            prompt_len = len(payload[0][0])
            for n in range(prompt_len, total + 1, 2):
                snapshot(payload, upto=n, cursor=True, ms=45)
            snapshot(payload, upto=total, cursor=True, ms=400)
            lines.append(payload)

    out = ROOT / "docs" / "demo.gif"
    out.parent.mkdir(exist_ok=True)
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=64) for f in frames]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True, disposal=1)
    print("wrote", out, len(frames), "frames", out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
