import copy


class GameLogic:
    """ Class of logic game
    """

    def __init__(self):
        self.x_pos = 1             # x position in matrix
        self.y_pos = 1             # y position in matrix
        self.count_moves = 0       # total of moves make along game
        self.game_states = []      # all game states of one game
        self.player_flag = False   # flag to know the player's turn
        self.end_game = False      # flag to find out if the game has come to an end

    def update_player(self) -> None:
        """ Updates which player to play """
        self.player_flag = not self.player_flag

    def has_victory(self, board, y, x) -> bool:
        """ Check if player has victory """
        return (
                (board[0][x] == board[1][x] == board[2][x])                    # check horizontal line
                or (board[y][0] == board[y][1] == board[y][2])                 # check vertical line
                or (x == y and board[0][0] == board[1][1] == board[2][2])      # check diagonal
                or (x + y == 2 and board[0][2] == board[1][1] == board[2][0])  # check diagonal
        )

    def update_move(self, board_game) -> None:
        """ Update the game logic for each move """
        # Update number of moves
        self.count_moves += 1
        # Save each game state
        self.game_states.append(copy.deepcopy(board_game))

    def update_input_positions(self, key) -> None:
        """ Update the game logic for each arrow input key """
        if key == "KEY_UP":
            self.y_pos = max(0, self.y_pos - 1)
        elif key == "KEY_DOWN":
            self.y_pos = min(2, self.y_pos + 1)
        elif key == "KEY_LEFT":
            self.x_pos = max(0, self.x_pos - 1)
        elif key == "KEY_RIGHT":
            self.x_pos = min(2, self.x_pos + 1)

