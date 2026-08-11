#!/usr/bin/env python3
"""ASCII-dither pass: unify the 10 generated frames into one visual system.

Each image -> grayscale -> luminance-to-character ramp at fixed column count.
Same ramp, same width, same dark canvas = one cohesive freeze-frame story,
regardless of generation variance. Output: slide-NN.txt per frame.
"""
import os
from PIL import Image

SRC = r"C:\Users\admin\casecraft-media\gen"
COLS = 210
ROWS = 74
RAMP = " .·:+=×#@"   # darkest -> brightest (8 levels)

def to_ascii(path, cols, rows):
    img = Image.open(path).convert("L")
    # fit width = cols, height scaled by aspect, then crop/pad to rows
    w, h = img.size
    aspect = h / w
    new_h = int(cols * aspect)
    img = img.resize((cols, new_h))
    if new_h > rows:
        top = (new_h - rows) // 2
        img = img.crop((0, top, cols, top + rows))
    else:
        canvas = Image.new("L", (cols, rows), 0)
        canvas.paste(img, (0, (rows - new_h) // 2))
        img = canvas
    px = list(img.getdata())
    lines = []
    for r in range(rows):
        line = "".join(RAMP[min(7, int(px[r * cols + c] / 256 * 8))]
                       for c in range(cols))
        lines.append(line.rstrip())
    return "\n".join(lines)

def main():
    for i in range(1, 11):
        png = os.path.join(SRC, f"slide-{i:02d}.png")
        if not os.path.exists(png):
            print(f"skip {i:02d}: missing")
            continue
        txt = to_ascii(png, COLS, ROWS)
        out = os.path.join(SRC, f"slide-{i:02d}.txt")
        with open(out, "w", encoding="utf-8") as f:
            f.write(txt)
        # quick quality probe: fraction of non-space chars
        nonspace = sum(1 for ch in txt if ch != " ")
        print(f"slide-{i:02d}: {os.path.getsize(png)//1024} KB -> "
              f"{len(txt.splitlines())} rows, density {100*nonspace//len(txt)}%")

if __name__ == "__main__":
    main()
