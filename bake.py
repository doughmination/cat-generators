#!/usr/bin/env python3

import re
from pathlib import Path

import numpy as np
from PIL import Image

ONEKO = Path(__file__).resolve().parent / "assets"
SRC = ONEKO / "classic.png"

MODES = {
    "gold.png":     "invert(75%) sepia(85%) saturate(1400%) hue-rotate(8deg) brightness(1.0)",
    "sapphire.png": "invert(45%) sepia(90%) saturate(2500%) hue-rotate(200deg) brightness(1.0)",
    "dusty.png":    "invert(60%)",
}


def clamp(rgb):
    return np.clip(rgb, 0.0, 1.0)


def apply_matrix(rgb, m):
    return clamp(rgb @ m.T)


def f_invert(rgb, a):
    # SVG tableValues "a 1-a" per channel -> out = a + (1-2a)*v
    return clamp(a + (1.0 - 2.0 * a) * rgb)


def f_brightness(rgb, b):
    return clamp(rgb * b)


def f_saturate(rgb, s):
    m = np.array([
        [0.213 + 0.787 * s, 0.715 - 0.715 * s, 0.072 - 0.072 * s],
        [0.213 - 0.213 * s, 0.715 + 0.285 * s, 0.072 - 0.072 * s],
        [0.213 - 0.213 * s, 0.715 - 0.715 * s, 0.072 + 0.928 * s],
    ])
    return apply_matrix(rgb, m)


def f_sepia(rgb, a):
    inv = 1.0 - a
    m = np.array([
        [0.393 + 0.607 * inv, 0.769 - 0.769 * inv, 0.189 - 0.189 * inv],
        [0.349 - 0.349 * inv, 0.686 + 0.314 * inv, 0.168 - 0.168 * inv],
        [0.272 - 0.272 * inv, 0.534 - 0.534 * inv, 0.131 + 0.869 * inv],
    ])
    return apply_matrix(rgb, m)


def f_hue_rotate(rgb, deg):
    a = np.deg2rad(deg)
    c, s = np.cos(a), np.sin(a)
    m = np.array([
        [0.213 + c * 0.787 - s * 0.213,
         0.715 - c * 0.715 - s * 0.715,
         0.072 - c * 0.072 + s * 0.928],
        [0.213 - c * 0.213 + s * 0.143,
         0.715 + c * 0.285 + s * 0.140,
         0.072 - c * 0.072 - s * 0.283],
        [0.213 - c * 0.213 - s * 0.787,
         0.715 - c * 0.715 + s * 0.715,
         0.072 + c * 0.928 + s * 0.072],
    ])
    return apply_matrix(rgb, m)


def parse_amount(val):
    val = val.strip()
    return float(val[:-1]) / 100.0 if val.endswith("%") else float(val)


def apply_chain(rgb, chain):
    for name, arg in re.findall(r"(\w[\w-]*)\(([^)]*)\)", chain):
        if name == "invert":
            rgb = f_invert(rgb, parse_amount(arg))
        elif name == "brightness":
            rgb = f_brightness(rgb, parse_amount(arg))
        elif name == "saturate":
            rgb = f_saturate(rgb, parse_amount(arg))
        elif name == "sepia":
            rgb = f_sepia(rgb, parse_amount(arg))
        elif name == "hue-rotate":
            rgb = f_hue_rotate(rgb, float(re.sub(r"deg$", "", arg.strip())))
        else:
            raise ValueError(f"unsupported filter: {name}")
    return rgb


def generate():
    base = Image.open(SRC).convert("RGBA")
    arr = np.asarray(base).astype(np.float64) / 255.0
    h, w, _ = arr.shape
    rgb0 = arr[:, :, :3].reshape(-1, 3)
    alpha = arr[:, :, 3]

    for fname, chain in MODES.items():
        out = apply_chain(rgb0.copy(), chain).reshape(h, w, 3)
        rgba = np.dstack([out, alpha])
        Image.fromarray((rgba * 255.0 + 0.5).astype(np.uint8), "RGBA").save(ONEKO / "output" / fname)
        print(f"wrote {fname}  <-  {chain}")


if __name__ == "__main__":
    generate()
