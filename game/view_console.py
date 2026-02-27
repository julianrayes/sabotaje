"""Console view: all terminal I/O for SABOTAJE.

Implements every display and input interaction for the console front-end.
Swapping this class with a GUI equivalent is all that is needed to port the
game to a graphical interface.
"""
from typing import List, Optional

from game.display import (
    SEPARATOR,
    clear_screen,
    press_enter,
    print_banner,
    wait_for_space,
)
from game.model import Player
from game.roles import Role

_NO_WORD = "(sin palabra)"


class ConsoleView:
    """Console implementation of the game UI.

    All stdout/stdin access is confined to this class so that the Controller
    and Model stay free of I/O code.
    """

    # ------------------------------------------------------------------ menus

    def show_main_menu(self) -> str:
        """Render main menu and return the user's raw choice string."""
        clear_screen()
        print_banner()
        print("  Bienvenido a SABOTAJE")
        print("  El juego de palabras con impostores – edición argentina\n")
        print(f"  {SEPARATOR}")
        print("    1. Jugar")
        print("    2. Salir")
        print(f"  {SEPARATOR}")
        return input("\n  Tu elección (1-2): ").strip()

    # ------------------------------------------------------------------ setup

    def ask_difficulty(self) -> str:
        options = {"1": "facil", "2": "medio", "3": "dificil"}
        print(f"\n{SEPARATOR}")
        print("  Seleccioná la dificultad:")
        print(SEPARATOR)
        print("    1. Fácil")
        print("    2. Medio")
        print("    3. Difícil")
        while True:
            choice = input("\n  Tu elección (1-3): ").strip()
            if choice in options:
                return options[choice]
            print("  ⚠  Opción inválida. Ingresá 1, 2 o 3.")

    def ask_player_count(self) -> int:
        while True:
            raw = input("\n  Ingresá el número de jugadores (3-10): ").strip()
            if raw.isdigit() and 3 <= int(raw) <= 10:
                return int(raw)
            print("  ⚠  El número debe estar entre 3 y 10.")

    def ask_player_names(self, n: int) -> List[str]:
        names: List[str] = []
        print(f"\n  Ingresá los nombres de los {n} jugadores:")
        for i in range(n):
            while True:
                name = input(f"    Jugador {i + 1}: ").strip()
                if name:
                    names.append(name)
                    break
                print("    ⚠  El nombre no puede estar vacío.")
        return names

    # ------------------------------------------------------------------ role reveal

    def show_player_call(self, name: str) -> None:
        """Tell the named player to take the device and press SPACE."""
        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  ¡Le toca a {name}!")
        print(SEPARATOR)
        print(f"\n  {name}, presioná ESPACIO para ver tu carta...")
        wait_for_space()

    def show_role_card(
        self, name: str, display_role: str, word: Optional[str]
    ) -> None:
        """Show the role card then wait for SPACE to hide it."""
        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  Rol     : {display_role}")
        print(f"  Palabra : {word if word is not None else _NO_WORD}")
        print(SEPARATOR)
        print("\n  ¡Recordá bien tu rol y tu palabra!")
        print("  Presioná ESPACIO para ocultar y pasar al siguiente jugador...")
        wait_for_space()

    def show_all_roles_done(self) -> None:
        clear_screen()
        print(f"\n{SEPARATOR}")
        print("  ¡Todos los jugadores ya conocen su rol!")
        print("  Pueden comenzar a discutir.")
        print(SEPARATOR)
        press_enter()

    # ------------------------------------------------------------------ game loop

    def show_game_status(self, alive: List[Player]) -> str:
        """Render in-progress game status and return the user's raw choice."""
        clear_screen()
        print(f"\n{SEPARATOR}")
        print("  SABOTAJE – Partida en curso")
        print(SEPARATOR)
        print(f"\n  Jugadores activos ({len(alive)}):")
        for p in alive:
            print(f"    - {p.name}")
        print("\n  Opciones:")
        print("    V – Votar al eliminado")
        print("    S – Salir al menú principal")
        return input("\n  Tu elección: ").strip().upper()

    def show_elimination_menu(self, alive: List[Player]) -> Player:
        """Show voting list and return the selected Player object."""
        print(f"\n{SEPARATOR}")
        print("  ¿A quién eliminan?")
        print(SEPARATOR)
        for i, p in enumerate(alive, 1):
            print(f"    {i}. {p.name}")
        while True:
            raw = input("\n  Número del jugador a eliminar: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(alive):
                return alive[int(raw) - 1]
            print(f"  ⚠  Ingresá un número entre 1 y {len(alive)}.")

    def show_eliminated_laburante(self, player: Player) -> None:
        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  {player.name} fue eliminado!")
        print(f"  Su rol era: {player.role.value}")
        print(SEPARATOR)
        print("\n  Era un LABURANTE. ¡El juego continúa!")
        press_enter()

    def show_eliminated_impostor(self, player: Player) -> None:
        """Show elimination reveal before the guess prompt."""
        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  {player.name} fue eliminado!")
        print(f"  Su rol era: {player.role.value}")
        if player.role == Role.DOPPELGANGER:
            print(f"  Su palabra era: {player.word}")
        print(SEPARATOR)
        print(f"\n  ¡Era un {player.role.value}!")
        print("\n  Tiene una última oportunidad de adivinar la palabra civil.")

    def ask_impostor_guess(self, player: Player) -> str:
        return input(f"  {player.name}, ¿cuál es la palabra civil? ").strip().lower()

    def show_guess_correct(self, civil_word: str) -> None:
        clear_screen()
        print(f"\n{SEPARATOR}")
        print(f"  ✅ ¡CORRECTO! La palabra era «{civil_word}».")
        print("  😈 ¡Los IMPOSTORES ganan!")
        print(SEPARATOR)
        press_enter("Presioná ENTER para volver al menú principal...")

    def show_guess_wrong(self, civil_word: str, remaining_count: int) -> None:
        print(f"\n  ❌ Incorrecto. La palabra civil era: «{civil_word}»")
        if remaining_count == 0:
            print("\n  No quedan más impostores. ¡Los LABURANTES ganan!")
            press_enter("Presioná ENTER para volver al menú principal...")
        else:
            print(
                f"\n  Quedan {remaining_count} impostor(es) en juego. "
                "¡El juego continúa!"
            )
            press_enter()

    def show_win(self, winner: str) -> None:
        """Display the final win screen."""
        clear_screen()
        print(f"\n{SEPARATOR}")
        if winner == "laburantes":
            print("  🎉 ¡Los LABURANTES ganan! Eliminaron a todos los impostores.")
        else:
            print("  😈 ¡Los IMPOSTORES ganan! Son tantos o más que los laburantes.")
        print(SEPARATOR)
        press_enter("Presioná ENTER para volver al menú principal...")

    def show_farewell(self) -> None:
        print("\n  ¡Hasta la próxima!\n")
