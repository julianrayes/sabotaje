#!/usr/bin/env python3
"""SABOTAJE – Juego de palabras con impostores. Punto de entrada."""
from game.controller import GameController
from game.view_console import ConsoleView


def main() -> None:
    view = ConsoleView()
    controller = GameController(view)
    controller.run()


if __name__ == "__main__":
    main()
