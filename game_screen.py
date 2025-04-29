
import pygame
import time
from utils.button import Button
from puzzle import PuzzleBoard
from A_star import a_star, manhattan_distance, misplaced_tiles, tiles_out_of_row_and_column
import os
import random
import copy

""" Thiết kế các nút chức năng """
image_btn =   Button((0,  80, 200, 60), "IMAGE")
support_btn = Button((0, 140, 200, 60), "SUPPORT")
reset_btn =   Button((0, 200, 200, 60), "PLAY AGAIN")
quit_btn =    Button((0, 260, 200, 60), "MENU")
heuristic_btn = Button((800, 80, 200, 60), "HEURISTIC")
font = pygame.font.SysFont("Times New Roman", 28, True)

""" Hàm vẽ màn hình game """
def draw_game_screen(screen, game_data): 
    screen.fill((30, 30, 30))

    # Sidebar trái
    sidebar = pygame.Rect(0, 0, screen.get_width() // 5, screen.get_height()) # Vị trí (0,0) - góc trên bên trái, rộng = 1/4 rộng màn hình, cao = cao màn hình
    pygame.draw.rect(screen, (230, 230, 250), sidebar)
    # Sidebar phải 
    sidebar_right = pygame.Rect( screen.get_width() * 4 // 5,  0,screen.get_width() // 5,  screen.get_height() )
    pygame.draw.rect(screen, (230, 230, 250), sidebar_right)


    # Tính thời gian chơi game
    if game_data.get("solved"):
        elapsed = int(game_data["end_time"] - game_data["start_time"])
    else:
        elapsed = int(time.time() - game_data["start_time"]) # Tính thời gian đã trôi qua kể từ khi bắt đầu trò chơi bằng cách lấy thời gian hiện tại trừ đi thời gian bắt đầu được lưu trong game_data.
    time_txt = font.render(f" Time: {elapsed}s", True, (0, 0, 0))
    screen.blit(time_txt, (30, 10))

    for button in [image_btn, support_btn, reset_btn, quit_btn, heuristic_btn]:
        button.check_hover(pygame.mouse.get_pos())
        button.draw(screen)

    draw_board(game_data['board'], screen, game_data)  # Gọi hàm để vẽ trạng thái hiện tại của bảng trò chơi lên màn hình
    
    # Hiển thị hình gốc
    image = pygame.transform.scale(game_data["original_image"], (180, 180))
    image_rect = image.get_rect(center=(sidebar.centerx, 420))
    screen.blit(image, image_rect)

    font_s = pygame.font.SysFont("Times New Roman", 23)
    if "compare_results" in game_data:
        y = 160  # điểm bắt đầu vẽ bên phải
        for algo, (steps, explored, time_taken) in game_data["compare_results"].items():
            # In tên thuật toán
            text_algo = font.render(f"{algo}:", True, (0, 0, 0))
            screen.blit(text_algo, (screen.get_width() - 200, y))
            y += 25

            # In số bước
            text_steps = font_s.render(f"Bước: {steps}", True, (0, 0, 0))
            screen.blit(text_steps, (screen.get_width() - 195, y))
            y += 25

            # In số nút duyệt
            text_explored = font_s.render(f"Nút duyệt: {explored}", True, (0, 0, 0))
            screen.blit(text_explored, (screen.get_width() - 195, y))
            y += 25

            # In thời gian
            text_time = font_s.render(f"Thời gian: {time_taken}s", True, (0, 0, 0))
            screen.blit(text_time, (screen.get_width() - 195, y))
            y += 35  # thêm khoảng cách trước khi in thuật toán tiếp theo


    # Hiển thị thông báo hoàn thành
    if game_data.get("solved"):
        font_big = pygame.font.SysFont("Times New Roman", 40, True)
        win_text = font_big.render(" ! Bạn đã hoàn thành !", True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(screen.get_width() * 1.5 // 3, screen.get_height() // 2))
        screen.blit(win_text, text_rect)

    image = pygame.image.load("Image/puzzle.png")
    image = pygame.transform.scale(image, (80, 80))  
    screen.blit(image, (860, 5))

""" Hàm vẽ bảng trò chơi"""
def draw_board(puzzle_board, screen, game_data):
    board = puzzle_board.board
    empty_pos = puzzle_board.empty_pos
    grid_size = len(board)
    margin = 4
    font = pygame.font.SysFont(None, 48)

    # Vùng chơi ở giữa
    board_width = screen.get_width() * 3 // 4
    board_height = screen.get_height()
    tile_size = min(board_width // grid_size, board_height // grid_size) 

    start_x = screen.get_width() // 5 + 50
    start_y = 5

    for i in range(grid_size):
        for j in range(grid_size):
            value = board[i][j]

            rect = pygame.Rect(
                start_x + j * tile_size + margin,
                start_y + i * tile_size + margin,
                tile_size - 2 * margin,
                tile_size - 2 * margin
            )

            if value != 0 and game_data.get("tiles"):
                try:
                    tile_image = game_data["tiles"][value - 1]
                    screen.blit(pygame.transform.scale(tile_image, rect.size), rect)
                except IndexError:
                    # fallback nếu danh sách tiles không đúng
                    pygame.draw.rect(screen, (200, 200, 255), rect)
                    text = font.render(str(value), True, (0, 0, 0))
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, (50, 50, 50), rect)

    # Hiển thị số bước
    font_step = pygame.font.SysFont("Times New Roman", 28, True)
    step_text = font_step.render(f"Steps: {puzzle_board.move_count}", True, (0, 0, 0))
    screen.blit(step_text, (40, 40))
    

""" Hàm click chuột để di chuyển trò chơi """
def click_to_move(puzzle_board, pos, screen):
    board = puzzle_board.board
    # Tính toán kích thước vùng chơi bên phải
    board_width = screen.get_width() * 3 // 4
    board_height = screen.get_height()
    grid_size = len(board)
    # Tính toán kích thước mỗi ô
    tile_size = min(board_width // grid_size, board_height // grid_size) 
    margin = 4 # khoảng cách giữa các ô
    start_x = screen.get_width() // 4 + 50
    start_y = 5

    # Chuyển tọa độ chuột về vị trí trong bảng
    col = (pos[0] - start_x) // tile_size
    row = (pos[1] - start_y) // tile_size

    if not (0 <= row < len(board) and 0 <= col < len(board)):
        return  # click ngoài bảng

    if 0 <= row < grid_size and 0 <= col < grid_size:
        puzzle_board.move_tile((row, col))  # ✅ Dùng đúng method để tăng move_count

""" Hàm xử lý sự kiện ở các nút"""
def handle_game_events(event, game_data, reset_callback,set_state):
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        if support_btn.is_clicked(pos):
            run_ai_solution(pygame.display.get_surface(), game_data)
        elif reset_btn.is_clicked(pos):
            reset_callback()
            PuzzleBoard.move_count = 0
            game_data.pop("compare_results", None)
        elif quit_btn.is_clicked(pos):
            set_state("start")
            game_data.pop("compare_results", None)
        elif image_btn.is_clicked(pos):
            choose_image(game_data)
        elif heuristic_btn.is_clicked(pos):
            compare_astar_heuristics(game_data)
        else:
            if game_data["board"]:
                click_to_move(game_data["board"], pos, pygame.display.get_surface())
        

        if game_data["board"].is_goal() and not game_data["solved"]:
            game_data["solved"] = True
            game_data["end_time"] = time.time()
            print("🎉 Bạn đã hoàn thành !")

""" Hàm chọn ảnh bất kì trong file ảnh """
def get_random_image(image_folder="images"):
    images = [f for f in os.listdir(image_folder) if f.endswith((".jpg", ".png"))]
    image_path = os.path.join(image_folder, random.choice(images))
    return image_path

""" Hàm load ảnh đã được chọn lên giao diện game"""
def load_tile_images(image_path, size, tile_size):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (tile_size * size, tile_size * size))

    tiles = {}
    count = 1
    for row in range(size):
        for col in range(size):
            if count < size * size:
                rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                sub_img = image.subsurface(rect).copy()
                tiles[count] = sub_img
                count += 1
    return tiles, image  # tiles là dict: {1: img, 2: img, ..., size*size-1: img}

from tkinter import Tk, filedialog
from utils.image_utils import load_tile_images 

""" Hàm chọn ảnh"""

def choose_image(game_data):
    # Mở hộp thoại chọn ảnh
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ tkinter gốc
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")]
    )
    root.destroy()

    if filepath:
        size = game_data.get("size", 3)
        tile_size = 100

        try:
            # Load ảnh và chia thành tile
            tiles, original = load_tile_images(filepath, size, tile_size)

            # Cập nhật dữ liệu game
            game_data["tiles"] = tiles
            game_data["original_image"] = original

            # Xáo trộn board mới
            game_data["board"] = PuzzleBoard.generate_solvable_puzzle(size)
            game_data["start_time"] = time.time()
            game_data["solved"] = False

            print("Đã chọn ảnh:", filepath)

        except Exception as e:
            print("Lỗi khi xử lý ảnh:", e)

"""Hàm thiết lập các tham số và trạng thái ban đầu """
def setup_game(game_data):
    size = game_data.get("size", 3) # lấy kích thước của bảng trò chơi từ game_data
    tile_size = 100

    game_data['start_time'] = time.time() # thời gian bắt đầu trò chơi
    game_data['board'] = PuzzleBoard.generate_solvable_puzzle(size, steps=100) # Tạo bảng puzzle

    image_path = get_random_image("images")   # Chọn và tải hình ảnh ngẫu nhiên
    tiles, original_image = load_tile_images(image_path, size, tile_size) #Tải và chia nhỏ hình ảnh
    
    #Cập nhật dữ liệu 
    game_data['move_count'] = -1
    game_data["tiles"] = tiles  # dict: {1: img, ..., size*size - 1: img}
    game_data["original_image"] = original_image
    game_data["solved"] = False
    game_data["end_time"] = None

""" Hàm chạy thuật toán tìm solution"""
def run_ai_solution(screen, game_data):
    board = game_data["board"]
    if board.is_goal():
        print("Đã hoàn thành rồi!")
        return

    print("🔍 AI đang tìm lời giải...")

    solution = a_star(board, heuristic_func=manhattan_distance) # Gọi thuật toán A* với manhattan để chạy

    if solution is None:
        print("❌ Không tìm được lời giải.")
        return

    print(f"✅ Đã tìm được lời giải với {len(solution)} bước.")

    # Hiển thị các bước chạy thuật toán
    for step in solution:
        game_data["board"].board = [row[:] for row in step.board]  # Copy board
        game_data["board"].empty_pos = step.empty_pos
        game_data["board"].move_count += 1  # Cộng dồn số bước

        draw_game_screen(screen, game_data)
        pygame.display.update()
        pygame.time.delay(500)  # Delay mỗi bước 1000ms

""" Hàm chạy các hàm heuristic"""
def compare_astar_heuristics(game_data):
    base = PuzzleBoard(copy.deepcopy(game_data["board"].board)) # lấy board hiện tại

    results = {}

    # Manhattan
    start = time.time()
    path_manhattan, explored_manhattan = a_star(base, heuristic_func=manhattan_distance, return_explored=True)
    end = time.time()
    steps_manhattan = len(path_manhattan) if path_manhattan else 0
    time_manhattan = round(end - start, 4)
    results["Manhattan"] = (steps_manhattan, explored_manhattan, time_manhattan)

    # Misplaced Tiles
    start = time.time()
    path_misplaced, explored_misplaced = a_star(base, heuristic_func=misplaced_tiles, return_explored=True)
    end = time.time()
    steps_misplaced = len(path_misplaced) if path_misplaced else 0
    time_misplaced = round(end - start, 4)
    results["Misplaced"] = (steps_misplaced, explored_misplaced, time_misplaced)

    #  Tiles Out of Row/Column
    start = time.time()
    path_tiles_out, explored_tiles_out = a_star(base, heuristic_func=tiles_out_of_row_and_column, return_explored=True)
    end = time.time()
    steps_tiles_out = len(path_tiles_out) if path_tiles_out else 0
    time_tiles_out = round(end - start,4)
    results["Tiles Out"] = (steps_tiles_out,explored_tiles_out, time_tiles_out)
    
    # Lưu kết quả vào game_data
    game_data["compare_results"] = results