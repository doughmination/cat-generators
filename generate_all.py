from spirit import generate as ghost_gen
from bake import generate as bake
from apride import run

from pathlib import Path

BASE = Path(__file__).resolve().parent
folder = BASE / "assets" / "output" / "pride"

folder.mkdir(parents=True, exist_ok=True)

run()
bake()
ghost_gen()