from collections import deque

SIZE = 10
BLACK = 1
WHITE = 0
VISITED = 2
N = -1


class Position:
    def __init__(self, i, j, color):
        self.I = i
        self.J = j
        self.Color = color

    def equals(self, other):
        return self.I == other.I and self.J == other.J and self.Color == other.Color


def new_position(i, j, color):
    return Position(i, j, color)


def first_step(board, pos):
    # move right
    if SIZE > pos.J + 2:
        if board[pos.I][pos.J + 1] != BLACK:
            return new_position(pos.I, pos.J + 1, board[pos.I][pos.J + 1])
    # move left
    if 0 <= pos.J - 2:
        if board[pos.I][pos.J - 1] != BLACK:
            return new_position(pos.I, pos.J - 1, board[pos.I][pos.J - 1])
    # move up
    if 0 <= pos.I - 2:
        if board[pos.I - 1][pos.J] != BLACK:
            return new_position(pos.I - 1, pos.J, board[pos.I - 1][pos.J])
    # move down
    if SIZE > pos.I + 2:
        if board[pos.I + 1][pos.J] != BLACK:
            return new_position(pos.I + 1, pos.J, board[pos.I + 1][pos.J])

    return new_position(N, N, N)


def contains(vector, pos):
    for p in vector:
        if p.equals(pos):
            return True
    return False


def find_next_positions(board, pos, prev_pos, checked_positions, start_pos):
    positions = []
    if prev_pos.Color == BLACK:
        if pos.I - prev_pos.I == 1 and pos.I < SIZE:
            positions.append(new_position(pos.I + 1, pos.J, board[pos.I + 1][pos.J]))
        if pos.I - prev_pos.I == -1 and pos.I - 1 >= 0:
            positions.append(new_position(pos.I - 1, pos.J, board[pos.I - 1][pos.J]))
        if pos.J - prev_pos.J == 1 and pos.J + 1 < SIZE:
            positions.append(new_position(pos.I, pos.J + 1, board[pos.I][pos.J + 1]))
        if pos.J - prev_pos.J == -1 and pos.J - 1 >= 0:
            positions.append(new_position(pos.I, pos.J - 1, board[pos.I][pos.J - 1]))
        for item in checked_positions:
            if contains(positions, item):
                positions = [p for p in positions if not p.equals(item) or p.equals(start_pos)]
        return positions

    if board[pos.I][pos.J] == BLACK:
        if abs(pos.I - prev_pos.I) == 1.0:
            # move right
            if SIZE > pos.J + 2:
                if board[pos.I][pos.J + 1] != BLACK:
                    positions.append(new_position(pos.I, pos.J + 1, board[pos.I][pos.J + 1]))
            # move left
            if pos.J - 2 >= 0:
                if board[pos.I][pos.J - 1] != BLACK:
                    positions.append(new_position(pos.I, pos.J - 1, board[pos.I][pos.J - 1]))
        else:
            # move up
            if pos.I - 2 >= 0:
                if board[pos.I - 1][pos.J] != BLACK:
                    positions.append(new_position(pos.I - 1, pos.J, board[pos.I - 1][pos.J]))
            # move down
            if SIZE > pos.I + 2:
                if board[pos.I + 1][pos.J] != BLACK:
                    positions.append(new_position(pos.I + 1, pos.J, board[pos.I + 1][pos.J]))

    if board[pos.I][pos.J] == WHITE:
        if pos.I - prev_pos.I == 1:
            if pos.I + 1 < SIZE:
                if board[pos.I + 1][pos.J] == BLACK:
                    positions.append(new_position(pos.I + 1, pos.J, board[pos.I + 1][pos.J]))
        if pos.I - prev_pos.I == -1:
            if pos.I - 1 >= 0:
                if board[pos.I - 1][pos.J] == BLACK:
                    positions.append(new_position(pos.I - 1, pos.J, board[pos.I - 1][pos.J]))
        if pos.J - prev_pos.J == 1:
            if pos.J + 1 < SIZE:
                if board[pos.I][pos.J + 1] == BLACK:
                    positions.append(new_position(pos.I, pos.J + 1, board[pos.I][pos.J + 1]))
        if pos.J - prev_pos.J == -1:
            if pos.J - 1 >= 0:
                if board[pos.I][pos.J - 1] == BLACK:
                    positions.append(new_position(pos.I, pos.J - 1, board[pos.I][pos.J - 1]))

    for item in checked_positions:
        if contains(positions, item):
            positions = [p for p in positions if not p.equals(item)]
    return positions


def find_black_cells(board):
    blacks = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == BLACK:
                blacks.append(new_position(i, j, BLACK))
    return blacks


def loop(board, start_position):
    board_copy = [row[:] for row in board]
    prev_pos = start_position
    board_copy[prev_pos.I][prev_pos.J] = VISITED
    positions_to_check = deque()
    checked_positions = []
    first = first_step(board, prev_pos)
    if first.equals(new_position(N, N, N)):
        return None
    positions_to_check.append(first)
    prev_positions = {positions_to_check[0]: prev_pos}
    checked_positions.append(new_position(start_position.I, start_position.J, start_position.Color))
    while positions_to_check:
        pos = positions_to_check.pop()
        if pos.equals(start_position):
            for checked_pos in checked_positions:
                board_copy[checked_pos.I][checked_pos.J] = VISITED
            return board_copy
        checked_positions.append(pos)
        next_positions = find_next_positions(board, pos, prev_positions[pos], checked_positions, start_position)
        if not next_positions:
            if positions_to_check:
                while checked_positions[-1] != prev_positions[positions_to_check[-1]]:
                    checked_positions.pop()
                    if not checked_positions:
                        break
            else:
                break
        else:
            for position in next_positions:
                positions_to_check.append(position)
                prev_positions[position] = pos
    return None


class ICalculator:
    def find_loop(self, board):
        raise NotImplementedError


class Calculator(ICalculator):
    def find_loop(self, board):
        blacks = find_black_cells(board)
        for black in blacks:
            solution = loop(board, black)
            if solution is not None:
                return solution
        return None
