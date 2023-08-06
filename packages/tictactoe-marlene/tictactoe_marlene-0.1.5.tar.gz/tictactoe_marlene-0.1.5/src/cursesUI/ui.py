import curses
import enum

from cursesUI import constants as const
from cursesUI.base import TextUI
# from .base import TextUI
from logic.game import GameLogic


class Cell(enum.Enum):
    EMPTY = " "
    CH_X = "X"
    CH_O = "O"

    def __str__(self):
        return f'{self.value}'


class GameUI(TextUI):
    """ Class GameUI
        @:param TextUI from base file (TextUI - courses)
    """

    def __init__(self):
        super().__init__()
        self.board_game = [[Cell.EMPTY.__str__()] * const.NUM_COLUMNS for _ in range(const.NUM_LINES)]
        self.game = GameLogic()

    def print_title(self) -> None:
        """ Print title of game """
        self.screen.addstr(1,
                           6,
                           const.GAME_TITLE,
                           curses.A_BOLD and curses.A_UNDERLINE)

    def print_board(self) -> None:
        """ Print board of game """
        self.screen.addstr(2,
                           3,
                           const.GAME_CONTROLS)
        self.screen.addstr(const.Y_SHIFT,
                           const.X_SHIFT + 4,
                           f'{self.board_game[0][0]} │ {self.board_game[0][1]} │ {self.board_game[0][2]}')
        self.screen.addstr(const.Y_SHIFT + 1,
                           const.X_SHIFT + 4,
                           const.BOARD_GRID)
        self.screen.addstr(const.Y_SHIFT + 2,
                           const.X_SHIFT + 4,
                           f'{self.board_game[1][0]} │ {self.board_game[1][1]} │ {self.board_game[1][2]}')
        self.screen.addstr(const.Y_SHIFT + 3,
                           const.X_SHIFT + 4,
                           const.BOARD_GRID)
        self.screen.addstr(const.Y_SHIFT + 4,
                           const.X_SHIFT + 4,
                           f'{self.board_game[2][0]} │ {self.board_game[2][1]} │ {self.board_game[2][2]}')

    def print_players(self) -> None:
        """ Print identification of players in each move """
        self.screen.addstr(const.Y_SHIFT + 6,
                           const.X_SHIFT + 4,
                           f'Player {Cell.CH_X.__str__()}',
                           curses.A_BOLD and curses.A_UNDERLINE if self.game.player_flag == 0 else 0)
        self.screen.addstr(const.Y_SHIFT + 7,
                           const.X_SHIFT + 4,
                           f'Player {Cell.CH_O.__str__()}',
                           curses.A_BOLD and curses.A_UNDERLINE if self.game.player_flag == 1 else 0)

    def print_result(self) -> None:
        """ Print the result of the game. """
        if self.game.has_victory(self.board_game, self.game.y_pos, self.game.x_pos):
            self.screen.addstr(const.Y_SHIFT + 2,
                               const.X_SHIFT + 20,
                               (
                                   f'Player {Cell.CH_X.__str__()} wins'
                                   if self.game.player_flag
                                   else f'Player {Cell.CH_O.__str__()} wins'
                               ),
                               curses.A_REVERSE)
            self.screen.addstr(const.Y_SHIFT + 3,
                               const.X_SHIFT + 17,
                               const.MSG_QUIT,
                               curses.A_BLINK)
            self.game.end_game = True
            curses.curs_set(0)
        elif self.game.count_moves == const.MAX_MOVES:
            self.screen.addstr(const.Y_SHIFT + 2,
                               const.X_SHIFT + 20,
                               'Nobody win',
                               curses.A_REVERSE)
            self.screen.addstr(const.Y_SHIFT + 3,
                               const.X_SHIFT + 17,
                               const.MSG_QUIT,
                               curses.A_BLINK)
            self.game.end_game = True
            curses.curs_set(0)

    def switch_player(self) -> None:
        """ Switch and print the current player """
        self.game.update_player()
        self.print_players()

    def draw(self) -> None:
        """ Draw all the TUI of game """
        curses.resize_term(20, 50)
        self.screen.border()
        self.print_title()
        self.print_board()
        x_step = 4
        y_step = 2
        if not self.game.end_game:
            self.print_players()
            self.screen.move(const.Y_SHIFT + self.game.y_pos * y_step,
                             const.X_SHIFT + self.game.x_pos * x_step + 4)
        else:
            self.print_result()

    def move(self) -> None:
        """ Make the update of each move in game. """
        # Get x and y of screen
        y, x = self.screen.getyx()
        # Validates if the move can be done (empty cell)
        if self.screen.inch(y, x) == ord(Cell.EMPTY.__str__()):
            # Draw the new move
            self.board_game[self.game.y_pos][self.game.x_pos] = (
                Cell.CH_O.__str__()
                if self.game.player_flag
                else Cell.CH_X.__str__()
            )
            # Update game logic of each move
            self.game.update_move(self.board_game)
            # Check for results
            self.print_result()
            # Switch player
            self.switch_player()

    def input(self, key) -> None:
        """ All the input options for play the game. """
        if not self.game.end_game:
            # Update input for arrows
            self.game.update_input_positions(key)
            if key == Cell.EMPTY.__str__():
                self.move()
            elif key == "q" or key == "Q":
                self.stop()
        else:
            if key:
                self.stop()

