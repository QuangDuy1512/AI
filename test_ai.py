from A_star import a_star, manhattan_distance, misplaced_tiles
from puzzle import PuzzleBoard
import time

# Ví dụ một trạng thái puzzle
start = PuzzleBoard([
    [8, 6, 7],
    [2, 5, 4],
    [3, 0, 1]
])

print("=== So sánh heuristic ===")

start_time = time.time()
print("👉 A* với Manhattan:")
solution1 = a_star(start, heuristic_func=manhattan_distance)
print("Số bước:", len(solution1) - 1 if solution1 else "Không tìm được")
print("⏱ Thời gian Manhattan:", time.time() - start_time)

start_time = time.time()
print("\n👉 A* với Misplaced Tiles:")
solution2 = a_star(start, heuristic_func=misplaced_tiles)
print("Số bước:", len(solution2) - 1 if solution2 else "Không tìm được")
print("⏱ Thời gian Misplaced:", time.time() - start_time)
