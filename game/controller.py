"""Game controller: orchestrates model and view.

The controller contains no display or input code.  All I/O goes through the
view, and all game state lives in the model.  To add a GUI, replace
ConsoleView with a class that implements the same interface.
"""
import sys

from game.model import GameState
from game.view_console import ConsoleView


class GameController:
    """Wires together GameState (model) and ConsoleView (view)."""

    def __init__(self, view: ConsoleView) -> None:
        self.view = view

    # ------------------------------------------------------------------ public

    def run(self) -> None:
        """Main loop: show menu and dispatch actions."""
        while True:
            choice = self.view.show_main_menu()
            if choice == "1":
                self._play_game()
            elif choice == "2":
                self.view.show_farewell()
                sys.exit(0)

    # ------------------------------------------------------------------ private

    def _play_game(self) -> None:
        difficulty, names = self._setup()
        state = GameState.build(names, difficulty)
        self._role_reveal(state)
        self._game_loop(state)

    def _setup(self) -> tuple:
        difficulty = self.view.ask_difficulty()
        n = self.view.ask_player_count()
        names = self.view.ask_player_names(n)
        return difficulty, names

    def _role_reveal(self, state: GameState) -> None:
        for player in state.players:
            self.view.show_player_call(player.name)
            self.view.show_role_card(player.name, player.display_role, player.word)
        self.view.show_all_roles_done()

    def _game_loop(self, state: GameState) -> None:
        while True:
            winner = state.check_win()
            if winner:
                self.view.show_win(winner)
                return

            choice = self.view.show_game_status(state.alive_players())
            if choice == "S":
                return
            elif choice == "V":
                if self._vote(state):
                    return

    def _vote(self, state: GameState) -> bool:
        """Handle one voting round. Returns True when the game ends."""
        alive = state.alive_players()
        player = self.view.show_elimination_menu(alive)
        state.eliminate(player)

        if not player.is_impostor:
            self.view.show_eliminated_laburante(player)
            return False

        self.view.show_eliminated_impostor(player)
        guess = self.view.ask_impostor_guess(player)

        if guess == state.civil_word.lower():
            self.view.show_guess_correct(state.civil_word)
            return True

        remaining = len(state.alive_impostors())
        self.view.show_guess_wrong(state.civil_word, remaining)
        return remaining == 0
