"""Load and query word pairs from the CSV database."""
import csv
import os
import random
from typing import Tuple, List

_DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "palabras.csv",
)

# Valid difficulty keys
DIFFICULTIES = {"facil", "medio", "dificil"}


def load_words(difficulty: str) -> List[Tuple[str, str]]:
    """Return all (civil, doppelganger) pairs for the requested difficulty."""
    if difficulty not in DIFFICULTIES:
        raise ValueError(
            f"Dificultad inválida: '{difficulty}'. "
            f"Usá una de: {', '.join(sorted(DIFFICULTIES))}"
        )
    pairs: List[Tuple[str, str]] = []
    with open(_DATA_FILE, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row["dificultad"].strip().lower() == difficulty:
                pairs.append((row["civil"].strip(), row["doppelganger"].strip()))
    return pairs


def get_random_pair(difficulty: str) -> Tuple[str, str]:
    """Return a random (civil_word, doppelganger_word) for the given difficulty."""
    pairs = load_words(difficulty)
    if not pairs:
        raise ValueError(
            f"No se encontraron palabras para la dificultad: '{difficulty}'"
        )
    return random.choice(pairs)
