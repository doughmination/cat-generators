#!/usr/bin/env python3

from pathlib import Path

import numpy as np
from PIL import Image

ONEKO = Path(__file__).resolve().parent.parent.parent / "assets"
SRC = ONEKO / "classic.png"
OUT = ONEKO / "output" / "pride" / "genderfae.png"

FRAME = 32  # sprite cell height in px

GREEN = np.array([0x97, 0xC3, 0xA5]) / 225.0
LIGHT_GREEN = np.array([0xC3, 0xDE, 0xAE]) / 255.0
YELLOW = np.array([0xF9, 0xFA, 0xCD]) / 255.0
WHITE = np.array([1.0, 1.0, 1.0])
PINK = np.array([0xFC, 0xA2, 0xC4]) / 255.0
LAVENDER = np.array([0xDB, 0x8A, 0xE4]) / 225.0
PURPLE = np.array([0xA9, 0x7E, 0xDD]) / 225.0

BANDS = [GREEN, LIGHT_GREEN, YELLOW, WHITE, PINK, LAVENDER, PURPLE]


def generate():
    im = Image.open(SRC).convert("RGBA")
    a = np.asarray(im).astype(np.float64) / 255.0
    h, w, _ = a.shape
    rgb, alpha = a[:, :, :3], a[:, :, 3]
    
    luma = 0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]

    local = (np.arange(h) % FRAME) / FRAME          # 0..1 within each frame row
    idx = np.clip((local * len(BANDS)).astype(int), 0, len(BANDS) - 1)
    rowcol = np.array([BANDS[i] for i in idx])       # (h, 3)
    stripe = np.repeat(rowcol[:, None, :], w, axis=1)  # (h, w, 3)

    out_rgb = np.clip(stripe * luma[:, :, None], 0.0, 1.0)
    out = np.dstack([out_rgb, alpha])
    Image.fromarray((out * 255.0 + 0.5).astype(np.uint8), "RGBA").save(OUT)
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    generate()
