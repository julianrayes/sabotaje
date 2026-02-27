"""Intelligent impostor count selection and role-type assignment."""
import random
from typing import List


# Probability rules: {n_players: ([counts], [weights])}
_RULES = {
    3:  ([1],    [100]),
    4:  ([1],    [100]),
    5:  ([1, 2], [50, 50]),
    6:  ([1, 2], [20, 80]),
    7:  ([2, 3], [40, 60]),
    8:  ([2, 3], [20, 80]),
    9:  ([3, 4], [40, 60]),
    10: ([3, 4], [20, 80]),
}


def select_impostor_count(n_players: int) -> int:
    """Intelligently select the number of impostors based on player count.

    Rules (as specified):
    - 3-4 players : always 1 impostor
    - 5 players   : 1 or 2, 50 / 50
    - 6 players   : 1 or 2, 20 / 80
    - 7 players   : 2 or 3, 40 / 60
    - 8 players   : 2 or 3, 20 / 80
    - 9 players   : 3 or 4, 40 / 60
    - 10 players  : 3 or 4, 20 / 80
    """
    if n_players not in _RULES:
        raise ValueError(f"Número de jugadores no soportado: {n_players}")
    counts, weights = _RULES[n_players]
    return random.choices(counts, weights=weights)[0]


def assign_role_types(n_impostors: int) -> List[str]:
    """Distribute n_impostors between IMPOSTOR and DOPPELGANGER types.

    Each of the (n_impostors + 1) possible splits has equal probability:
      - 0 DOPPELGANGER  / n IMPOSTOR
      - 1 DOPPELGANGER  / (n-1) IMPOSTOR
      - ...
      - n DOPPELGANGER  / 0 IMPOSTOR

    Returns a shuffled list of role-name strings.
    """
    n_doppelgangers = random.randint(0, n_impostors)
    n_true_impostors = n_impostors - n_doppelgangers
    roles = ["IMPOSTOR"] * n_true_impostors + ["DOPPELGANGER"] * n_doppelgangers
    random.shuffle(roles)
    return roles
