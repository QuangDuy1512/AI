import heapq
from puzzle import PuzzleBoard
from itertools import count  # <- dùng để tạo biến đếm duy nhất

def manhattan_distance(board):
    distance = 0
    size = board.size
    for i in range(size):
        for j in range(size):
            value = board.board[i][j]
            if value != 0:
                target_x = (value - 1) // size
                target_y = (value - 1) % size
                distance += abs(i - target_x) + abs(j - target_y)
    return distance

def a_star(start_board):
    open_set = []
    counter = count()  # đếm số thứ tự

    heapq.heappush(open_set, (0, next(counter), start_board))
    
    came_from = {}
    g_score = {start_board.serialize(): 0}
    
    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current.is_goal():
            return reconstruct_path(came_from, current)

        for neighbor in current.get_neighbors():
            neighbor_key = neighbor.serialize()
            tentative_g = g_score[current.serialize()] + 1

            if neighbor_key not in g_score or tentative_g < g_score[neighbor_key]:
                came_from[neighbor_key] = current
                g_score[neighbor_key] = tentative_g
                f = tentative_g + manhattan_distance(neighbor)
                heapq.heappush(open_set, (f, next(counter), neighbor))  # thêm biến đếm để so sánh
    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current.serialize() in came_from:
        current = came_from[current.serialize()]
        path.append(current)
    return path[::-1]
