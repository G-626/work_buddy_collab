#!/usr/bin/env python3
"""Generate the 10 CaseCraft story-frame backgrounds (Pollinations, free, no key).

Cohesion strategy: every prompt shares one style suffix (charcoal monochrome on
near-black, single warm-gold light upper-left), then the ASCII-dither pass in
ascii_ify.py unifies them further regardless of generation variance.
"""
import os, time, urllib.request, urllib.parse, sys
from PIL import Image

OUT = r"C:\Users\admin\casecraft-media\gen"
os.makedirs(OUT, exist_ok=True)

SUFFIX = ("monochrome charcoal on near-black background, single faint warm gold "
          "light source from upper left, cinematic, ethereal, minimalist, "
          "fine-art, dark editorial")

MOTIFS = [
    "two hands reaching toward each other from opposite edges of the frame, "
    "fingers almost touching, a tiny gap of warm light between the fingertips",
    "a shattered mirror, a faint silhouette in fragments drifting apart in dark "
    "space, sharp glass shards catching faint light",
    "countless small glass shards flowing and converging toward one single "
    "point of warm light at the center",
    "a luminous circular orbit path around a faint glowing core, particles "
    "tracing arcs, motion frozen in time",
    "a dark minimalist workbench with a softly glowing screen and faint console "
    "light, still and quiet",
    "stacked thin translucent layers and strata of light separating dark "
    "planes, geological cross-section",
    "a monolithic shield gate in dark stone with hairline cracks of gold light",
    "delicate circuit lines and small relay nodes glowing faintly in the dark, "
    "schematic blueprint",
    "a tall narrow window of soft light breaking through dark stone walls",
    "two hands almost touching, fingers reaching across a gap, warm golden "
    "light between the fingertips, full frame",
]

def fetch(prompt, path, retries=3):
    url = ("https://image.pollinations.ai/prompt/" +
           urllib.parse.quote(prompt) + "?width=640&height=360&nologo=true")
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
            img = Image.open(path).convert("L")
            px = list(img.resize((64, 36)).getdata())
            mn, mx = min(px), max(px)
            if mx - mn < 30:
                print(f"  [{attempt}] too flat (range {mx-mn}) — retrying")
                time.sleep(3)
                continue
            return True
        except Exception as e:
            print(f"  [{attempt}] error: {str(e)[:100]}")
            time.sleep(5)
    return False

ok = 0
for i, motif in enumerate(MOTIFS, 1):
    prompt = motif + ", " + SUFFIX
    path = os.path.join(OUT, f"slide-{i:02d}.png")
    print(f"[{i}/10] generating…", flush=True)
    t0 = time.time()
    if fetch(prompt, path):
        ok += 1
        print(f"  ok in {time.time()-t0:.0f}s ({os.path.getsize(path)//1024} KB)")
    else:
        print(f"  FAILED after retries")
print(f"DONE: {ok}/10 images in {OUT}")
