import random
import logging
import json

from Puzzle.calculations import SIZE
from Puzzle.models import Boards
from Puzzle.serializers import BoardSerializer


class IBoardGenerator:
    def generate_boards(self):
        pass


class BoardGenerator(IBoardGenerator):
    def __init__(self, calculator):
        self.calculator = calculator

    def create_random_board(self, rows, cols):
        board = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
        return board

    def generate_boards(self):
        board_size = SIZE
        generated_boards = []
        for _ in range(2000):
            need_more_try = True
            board_array = []
            while need_more_try:
                board_array = self.create_random_board(board_size, board_size)
                solution = self.calculator.find_loop(board_array)
                if solution is not None:
                    need_more_try = False
                    break
            self.save_result(board_array, generated_boards)

        logging.info("Workable boards are successfully generated")

    def save_result(self, board_array, generated_boards):
        serializer = BoardSerializer(data={'data': json.dumps(board_array)})
        if not self.check_board_already_generated(generated_boards, board_array):
            generated_boards.append(board_array)
            if serializer.is_valid():
                serializer.save()

    def check_board_already_generated(self, generated_boards, board_to_add):
        if len(generated_boards) < 1:
            return False
        for generated_board in generated_boards:
            for i in range(SIZE):
                for j in range(SIZE):
                    if generated_board[i][j] != board_to_add[i][j]:
                        return False
        return True
