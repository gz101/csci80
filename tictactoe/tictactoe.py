"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None
N = 3


def initial_state() -> list[list[str]]:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def _count_X_and_Os(board: list[list[str]]) -> tuple[int, int]:
    """
    Helper function to count the number of Xs and Os on the board.
    """
    nXs, nOs = 0, 0

    # count number of Xs and 0s
    for r in range(N):
        for c in range(N):
            if board[r][c] == X:
                nXs += 1
            elif board[r][c] == O:
                nOs += 1
    return nXs, nOs


def player(board: list[list[str]]) -> str:
    """
    Returns player who has the next turn on a board.
    """

    nXs, nOs = _count_X_and_Os(board)

    # invariant of game: nXs >= nOs since alternate with X first
    if nXs == nOs:
        return X
    return O


def actions(board: list[list[str]]) -> list[tuple[int, int]]:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = []

    # count number of empty spaces
    for r in range(N):
        for c in range(N):
            if board[r][c] == EMPTY:
                possible.append((r, c))
    return possible


def result(board: list[list[str]], action: tuple[int, int]) -> list[list[str]]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    r, c = action

    # raise exception on illegal move
    if board[r][c] != EMPTY:
        raise ValidationError("Invalid move.")

    # construct a new board with the move executed
    result = deepcopy(board)
    result[r][c] = player(board)
    return result


def winner(board: list[list[str]]) -> str | None:
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for r in range(N):
        if board[r][0] == board[r][1] == board[r][2]:
            return board[r][0]

    # check cols
    for c in range(N):
        if board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]

    # check left diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    # check right diagonal
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # game in progress or tied
    return None


def terminal(board: list[list[str]]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) or len(actions(board)) == 0


def utility(board: list[list[str]]) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0


def _max_value(board: list[list[str]]) -> tuple[int, int]:
    """
    Helper function for minimax algorithm to calculate maximum.
    """
    v = float("-inf")

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, _min_value(result(board, action)))
    return v


def _min_value(board: list[list[str]]) -> tuple[int, int]:
    """
    Helper function for minimax algorithm to calculate minimum.
    """
    v = float("inf")

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, _max_value(result(board, action)))
    return v


def minimax(board: list[list[str]]) -> tuple[int, int] | None:
    """
    Returns the optimal action for the current player on the board.
    """
    # check if terminal
    if terminal(board):
        return None

    possible_actions = actions(board)
    m = len(possible_actions)
    values = [0] * m
    current_player = player(board)

    # determine whether to maximize or minimize
    helper_func = _min_value
    opt_func = max
    if current_player == O:
        helper_func = _max_value
        opt_func = min

    # fill values array
    for i in range(m):
        values[i] = helper_func(result(board, possible_actions[i]))

    # determine the optimal move
    return possible_actions[values.index(opt_func(values))]
