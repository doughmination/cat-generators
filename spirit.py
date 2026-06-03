#!/usr/bin/env python3

from pathlib import Path

import numpy as np
from PIL import Image

ONEKO = Path(__file__).resolve().parent / "assets"
SRC = ONEKO / "classic.png"
OUT = ONEKO / "output" / "ghostspirit.png"

BRIGHTNESS = 1.7
OPACITY = 0.55


def generate():
    im = Image.open(SRC).convert("RGBA")
    a = np.asarray(im).astype(np.float64) / 255.0
    rgb, alpha = a[:, :, :3], a[:, :, 3]

    # grayscale(1) — Rec.709 luma
    g = 0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]
    rgb = np.dstack([g, g, g])

    rgb = np.clip(rgb * BRIGHTNESS, 0.0, 1.0)   # brightness(1.7)
    alpha = alpha * OPACITY                       # opacity(0.55) -> alpha

    out = np.dstack([rgb, alpha])
    Image.fromarray((out * 255.0 + 0.5).astype(np.uint8), "RGBA").save(OUT)
    print(f"wrote {OUT.name}  (glow stays a runtime drop-shadow)")


if __name__ == "__main__":
    generate()
