"""Game model: pure state and business logic, no I/O."""
import random
from dataclasses import dataclass, field
from typing import List, Optional

from game.impostor_logic import assign_role_types, select_impostor_count
from game.roles import Role
from game.word_database import get_random_pair


@dataclass
class Player:
    name: str
    role: Role
    word: Optional[str]
    alive: bool = True

    @property
    def is_impostor(self) -> bool:
        return self.role != Role.LABURANTE

    @property
    def display_role(self) -> str:
        """What the player sees on their card.

        DOPPELGANGER is shown as LABURANTE — they don't know they are impostors.
        """
        return "LABURANTE" if self.role == Role.DOPPELGANGER else self.role.value


@dataclass
class GameState:
    players: List[Player] = field(default_factory=list)
    civil_word: str = ""
    difficulty: str = "facil"

    @classmethod
    def build(cls, names: List[str], difficulty: str) -> "GameState":
        """Create a fully initialised game state from player names and difficulty."""
        civil_word, doppelganger_word = get_random_pair(difficulty)
        n = len(names)
        n_impostors = select_impostor_count(n)
        impostor_types = assign_role_types(n_impostors)

        roles: List[Role] = [Role.LABURANTE] * (n - n_impostors)
        for rt in impostor_types:
            roles.append(Role[rt])
        random.shuffle(roles)

        shuffled_names = names[:]
        random.shuffle(shuffled_names)

        players = []
        for name, role in zip(shuffled_names, roles):
            if role == Role.LABURANTE:
                word: Optional[str] = civil_word
            elif role == Role.DOPPELGANGER:
                word = doppelganger_word
            else:
                word = None
            players.append(Player(name=name, role=role, word=word))

        return cls(players=players, civil_word=civil_word, difficulty=difficulty)

    # ------------------------------------------------------------------ query

    def alive_players(self) -> List[Player]:
        return [p for p in self.players if p.alive]

    def alive_impostors(self) -> List[Player]:
        return [p for p in self.alive_players() if p.is_impostor]

    def alive_civilians(self) -> List[Player]:
        return [p for p in self.alive_players() if not p.is_impostor]

    def check_win(self) -> Optional[str]:
        """Return 'laburantes', 'impostores', or None (game still on)."""
        if not self.alive_impostors():
            return "laburantes"
        if len(self.alive_impostors()) >= len(self.alive_civilians()):
            return "impostores"
        return None

    # ------------------------------------------------------------------ mutate

    def eliminate(self, player: Player) -> None:
        player.alive = False
