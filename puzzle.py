import copy
import random

class PuzzleBoard:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.empty_pos = self.find_empty()
        self.move_count = 0

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_goal(self):
        expected = list(range(1, self.size ** 2)) + [0]
        flat_board = sum(self.board, [])
        return flat_board == expected

    def serialize(self):
        return str(self.board)

    def copy(self):
        return PuzzleBoard(copy.deepcopy(self.board))

    def get_neighbors(self):
        neighbors = []
        x, y = self.empty_pos
        directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_board = self.copy()
                # Swap
                new_board.board[x][y], new_board.board[new_x][new_y] = new_board.board[new_x][new_y], new_board.board[x][y]
                new_board.empty_pos = (new_x, new_y)
                neighbors.append(new_board)
        return neighbors

    def print_board(self):
        for row in self.board:
            print(" ".join(str(n).rjust(2) for n in row))
        print()

    def generate_solvable_puzzle(size, steps=100):
    # Tạo trạng thái đích
        goal = [[(i * size + j + 1) % (size * size) for j in range(size)] for i in range(size)]
        board = PuzzleBoard(goal)

        for _ in range(steps):
            neighbors = board.get_neighbors()
            board = random.choice(neighbors)

        return board
    def heuristic(self):
        distance = 0
        size = self.size
        flat_board = sum(self.board, [])  # Chuyển board thành một danh sách 1D từ danh sách 2D

        for i in range(len(flat_board)):
            if flat_board[i] != 0:  # Bỏ qua ô trống
                goal_row, goal_col = divmod(flat_board[i] - 1, size)  # Vị trí mục tiêu của số
                current_row, current_col = divmod(i, size)  # Vị trí hiện tại của số
                distance += abs(goal_row - current_row) + abs(goal_col - current_col)  # Tính Manhattan distance

        return distance
    def move_tile(self, pos):
        row, col = pos
        empty_row, empty_col = self.empty_pos

        if abs(row - empty_row) + abs(col - empty_col) == 1:
            self.board[empty_row][empty_col], self.board[row][col] = self.board[row][col], self.board[empty_row][empty_col]
            self.empty_pos = (row, col)
            self.move_count += 1

