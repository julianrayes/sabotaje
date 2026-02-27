"""Console I/O utilities: clear screen, banner, keypress helpers."""
import os
import sys

SEPARATOR = "=" * 55

BANNER = r"""
 ____    _    ____   ___ _____  _    ___  _____
/ ___|  / \  | __ ) / _ \_   _|/ \  |_ _|| ____|
\___ \ / _ \ |  _ \| | | || | / _ \  | | |  _|
 ___) / ___ \| |_) | |_| || |/ ___ \ | | | |___
|____/_/   \_\____/ \___/ |_/_/   \_\|___||_____|
"""


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Print the game banner."""
    print(BANNER)


def wait_for_space() -> None:
    """Block until the user presses SPACE (single keypress, no Enter needed)."""
    if os.name == "nt":
        import msvcrt

        while True:
            key = msvcrt.getch()
            if key == b" ":
                break
    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == " ":
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def press_enter(message: str = "Presioná ENTER para continuar...") -> None:
    """Prompt the user to press Enter."""
    input(f"\n  {message}")
