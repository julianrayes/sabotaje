#!/usr/bin/env python3
"""SABOTAJE – Juego de palabras con impostores. Ambientado en Argentina.

Roles:
  LABURANTE   – civil; recibe la palabra real.
  DOPPELGANGER– impostor encubierto; recibe una palabra similar. No sabe que es
                impostor (su carta muestra "LABURANTE").
  IMPOSTOR    – sabe que es impostor; no recibe ninguna palabra.
"""
import random
import sys

from game.display import clear_screen, press_enter, print_banner, wait_for_space, SEPARATOR
from game.impostor_logic import assign_role_types, select_impostor_count
from game.roles import Role
from game.word_database import get_random_pair


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _display_role(role: Role) -> str:
    """Return what the player sees on their card.

    DOPPELGANGER players are shown as LABURANTE — they don't know they are
    impostors (that's the twist).
    """
    return "LABURANTE" if role == Role.DOPPELGANGER else role.value


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def _choose_difficulty() -> str:
    options = {"1": "facil", "2": "medio", "3": "dificil"}
    print(f"\n{SEPARATOR}")
    print("  Seleccioná la dificultad:")
    print(f"{SEPARATOR}")
    print("    1. Fácil")
    print("    2. Medio")
    print("    3. Difícil")
    while True:
        choice = input("\n  Tu elección (1-3): ").strip()
        if choice in options:
            return options[choice]
        print("  ⚠  Opción inválida. Ingresá 1, 2 o 3.")


def _collect_names(n: int) -> list:
    names = []
    print(f"\n  Ingresá los nombres de los {n} jugadores:")
    for i in range(n):
        while True:
            name = input(f"    Jugador {i + 1}: ").strip()
            if name:
                names.append(name)
                break
            print("    ⚠  El nombre no puede estar vacío.")
    return names


def setup_game() -> tuple:
    """Interactive setup. Returns (difficulty, player_names)."""
    clear_screen()
    print_banner()
    difficulty = _choose_difficulty()

    while True:
        raw = input("\n  Ingresá el número de jugadores (3-10): ").strip()
        if raw.isdigit() and 3 <= int(raw) <= 10:
            n_players = int(raw)
            break
        print("  ⚠  El número debe estar entre 3 y 10.")

    names = _collect_names(n_players)
    return difficulty, names


# ---------------------------------------------------------------------------
# Player list construction
# ---------------------------------------------------------------------------

def build_player_list(names: list, difficulty: str) -> tuple:
    """Build shuffled player list with roles assigned.

    Returns (players, civil_word) where *players* is a list of dicts:
        {name, role, word, alive}
    """
    n = len(names)
    civil_word, doppelganger_word = get_random_pair(difficulty)

    n_impostors = select_impostor_count(n)
    impostor_types = assign_role_types(n_impostors)

    # Build role list: civilians + impostors, then shuffle
    roles = [Role.LABURANTE] * (n - n_impostors)
    for rt in impostor_types:
        roles.append(Role[rt])
    random.shuffle(roles)

    # Shuffle play order
    shuffled_names = names[:]
    random.shuffle(shuffled_names)

    players = []
    for name, role in zip(shuffled_names, roles):
        if role == Role.LABURANTE:
            word = civil_word
        elif role == Role.DOPPELGANGER:
            word = doppelganger_word
        else:  # IMPOSTOR
            word = None
        players.append({"name": name, "role": role, "word": word, "alive": True})

    return players, civil_word


# ---------------------------------------------------------------------------
# Role reveal phase
# ---------------------------------------------------------------------------

def role_reveal_phase(players: list) -> None:
    """Each player privately reads their role card."""
    for player in players:
        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  ¡Le toca a {player['name']}!")
        print(SEPARATOR)
        print(f"\n  {player['name']}, presioná ESPACIO para ver tu carta...")
        wait_for_space()

        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  Rol     : {_display_role(player['role'])}")
        if player["word"] is not None:
            print(f"  Palabra : {player['word']}")
        else:
            print("  Palabra : (sin palabra)")
        print(SEPARATOR)
        print("\n  ¡Recordá bien tu rol y tu palabra!")
        print("  Presioná ESPACIO para ocultar y pasar al siguiente jugador...")
        wait_for_space()

    clear_screen()
    print(f"\n{SEPARATOR}")
    print("  ¡Todos los jugadores ya conocen su rol!")
    print("  Pueden comenzar a discutir.")
    print(SEPARATOR)
    press_enter()


# ---------------------------------------------------------------------------
# Win-condition check
# ---------------------------------------------------------------------------

def check_win_conditions(players: list):
    """Return a win-message string if the game is over, else None."""
    alive = [p for p in players if p["alive"]]
    impostors = [p for p in alive if p["role"] != Role.LABURANTE]
    laburantes = [p for p in alive if p["role"] == Role.LABURANTE]

    if not impostors:
        return "🎉 ¡Los LABURANTES ganan! Eliminaron a todos los impostores."
    if len(impostors) >= len(laburantes):
        return "😈 ¡Los IMPOSTORES ganan! Son tantos o más que los laburantes."
    return None


# ---------------------------------------------------------------------------
# Voting
# ---------------------------------------------------------------------------

def _pick_eliminated(alive: list) -> dict:
    print(f"\n{SEPARATOR}")
    print("  ¿A quién eliminan?")
    print(SEPARATOR)
    for i, p in enumerate(alive, 1):
        print(f"    {i}. {p['name']}")
    while True:
        raw = input("\n  Número del jugador a eliminar: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(alive):
            return alive[int(raw) - 1]
        print(f"  ⚠  Ingresá un número entre 1 y {len(alive)}.")


def vote_phase(players: list, civil_word: str) -> bool:
    """Handle one voting round.

    Returns True if the game ended inside this function, False otherwise.
    """
    alive = [p for p in players if p["alive"]]
    eliminated = _pick_eliminated(alive)
    eliminated["alive"] = False

    clear_screen()
    print(f"\n{SEPARATOR}")
    print(f"  {eliminated['name']} fue eliminado!")
    print(f"  Su rol era: {eliminated['role'].value}")
    print(SEPARATOR)

    if eliminated["role"] == Role.LABURANTE:
        print("\n  Era un LABURANTE. ¡El juego continúa!")
        press_enter()
        return False

    # ---- IMPOSTOR or DOPPELGANGER ----------------------------------------
    print(f"\n  ¡Era un {eliminated['role'].value}!")
    if eliminated["role"] == Role.DOPPELGANGER:
        print(f"  Su palabra era: {eliminated['word']}")

    print("\n  Tiene una última oportunidad de adivinar la palabra civil.")
    guess = input(f"  {eliminated['name']}, ¿cuál es la palabra civil? ").strip().lower()

    if guess == civil_word.lower():
        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  ✅ ¡CORRECTO! La palabra era «{civil_word}».")
        print("  😈 ¡Los IMPOSTORES ganan!")
        print(SEPARATOR)
        press_enter("Presioná ENTER para volver al menú principal...")
        return True  # game over

    print(f"\n  ❌ Incorrecto. La palabra civil era: «{civil_word}»")
    remaining = [p for p in players if p["alive"] and p["role"] != Role.LABURANTE]
    if not remaining:
        print("\n  No quedan más impostores. ¡Los LABURANTES ganan!")
        press_enter("Presioná ENTER para volver al menú principal...")
        return True  # game over

    print(f"\n  Quedan {len(remaining)} impostor(es) en juego. ¡El juego continúa!")
    press_enter()
    return False


# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------

def game_loop(players: list, civil_word: str) -> None:
    """Run the vote / win-check loop until the game ends."""
    while True:
        clear_screen()

        result = check_win_conditions(players)
        if result:
            print(f"\n{SEPARATOR}")
            print(f"  {result}")
            print(SEPARATOR)
            press_enter("Presioná ENTER para volver al menú principal...")
            return

        alive = [p for p in players if p["alive"]]
        print(f"\n{SEPARATOR}")
        print("  SABOTAJE – Partida en curso")
        print(SEPARATOR)
        print(f"\n  Jugadores activos ({len(alive)}):")
        for p in alive:
            print(f"    - {p['name']}")
        print(f"\n  Opciones:")
        print("    V – Votar al eliminado")
        print("    S – Salir al menú principal")

        choice = input("\n  Tu elección: ").strip().upper()

        if choice == "S":
            return
        elif choice == "V":
            game_over = vote_phase(players, civil_word)
            if game_over:
                return


# ---------------------------------------------------------------------------
# High-level play / menu
# ---------------------------------------------------------------------------

def play_game() -> None:
    """Run one full game session."""
    difficulty, player_names = setup_game()
    players, civil_word = build_player_list(player_names, difficulty)
    role_reveal_phase(players)
    game_loop(players, civil_word)


def main_menu() -> None:
    """Show the main menu and handle navigation."""
    while True:
        clear_screen()
        print_banner()
        print("  Bienvenido a SABOTAJE")
        print("  El juego de palabras con impostores – edición argentina\n")
        print(f"  {SEPARATOR}")
        print("    1. Jugar")
        print("    2. Salir")
        print(f"  {SEPARATOR}")

        choice = input("\n  Tu elección (1-2): ").strip()
        if choice == "1":
            play_game()
        elif choice == "2":
            print("\n  ¡Hasta la próxima!\n")
            sys.exit(0)
        else:
            print("  ⚠  Opción inválida.")
            press_enter()


if __name__ == "__main__":
    main_menu()
