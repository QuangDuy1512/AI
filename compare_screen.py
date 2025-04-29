import pygame
import time
from utils.button import Button
from A_star import a_star, manhattan_distance
from search_algorithms import  greedy_best_first
from puzzle import PuzzleBoard
import copy
import threading


font_title = pygame.font.SysFont("Times New Roman", 32, bold=True)
font_result = pygame.font.SysFont("Times New Roman", 24)

start_button = Button((75, 450, 350, 40), "START COMPARE")
back_button = Button((575, 450, 350, 40), "BACK")

""" Hàm vẽ bảng puzzle """
def draw_board(surface, puzzle_board, x, y, size=3, tile_size=70, gap=5):
    board = puzzle_board.board
    font = pygame.font.SysFont(None, 36)

    for row in range(size):
        for col in range(size):
            value = board[row][col]
            rect = pygame.Rect(x + col * (tile_size + gap), y + row * (tile_size + gap), tile_size, tile_size)
            if value == 0:
                pygame.draw.rect(surface, (30, 30, 30), rect)
            else:
                pygame.draw.rect(surface, (100, 149, 237), rect)
                text = font.render(str(value), True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

""" Hàm vẽ giao diện"""
def draw_compare_screen(screen, game_data):
    screen.fill((230, 230, 250))

    title1 = font_title.render("So sánh", True, (0, 0, 128))
    screen.blit(title1, (screen.get_width() // 2 - title1.get_width() // 2, 15))
    title = font_title.render("Thuật toán A* và Greedy Best-First Search", True, (0, 0, 128))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))

    # Vị trí cố định mỗi puzzle
    astar_x, astar_y = 140, 110
    greedy_x, greedy_y = 640, 110

    if "astar_current" in game_data:
        draw_board(screen, game_data["astar_current"], x=astar_x, y=astar_y)
    if "greedy_current" in game_data:
        draw_board(screen, game_data["greedy_current"], x=greedy_x, y=greedy_y)

    # Hiển thị kết quả nếu đã chạy xong
    if "astar_result" in game_data:
        result_text = font_result.render(game_data["astar_result"], True, (0, 0, 0))
        screen.blit(result_text, (320, 100 + 3 * 75 + 20))  # dưới puzzle

    if "greedy_result" in game_data:
        result_text = font_result.render(game_data["greedy_result"], True, (0, 0, 0))
        screen.blit(result_text, (320, 100 + 3 * 75 + 60))  # dưới puzzle

    for button in [back_button, start_button]:
        button.check_hover(pygame.mouse.get_pos())
        button.draw(screen)

    image1 = pygame.image.load("Image/feedback.png")
    image1 = pygame.transform.scale(image1, (70, 70))  # kích thước mới (rộng x cao)
    screen.blit(image1, (465, 140)) 

    pygame.display.update()

""" Hàm sự kiện """
def handle_compare_events(event, game_data,set_state):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if back_button.is_clicked(event.pos):
            set_state("start")
        if start_button.is_clicked(event.pos):
            run_ai_comparison(pygame.display.get_surface(), game_data)

""" Hàm chạy thuật toán """
def run_ai_comparison(screen, game_data):
    base_board = game_data["compare_base"]
    
    # Copy riêng cho mỗi thuật toán
    astar_board = copy.deepcopy(base_board)
    greedy_board = copy.deepcopy(base_board)

    # Các biến để lưu kết quả
    result_data = {"astar_done": False, "greedy_done": False}
    """ Hàm chạy thuật toán A* """
    def run_astar():
        start_astar = time.time()
        astar_path, astar_explored = a_star(astar_board, heuristic_func=manhattan_distance, return_explored=True)
        end_astar = time.time()
        astar_duration = round(end_astar - start_astar, 6)

        if astar_path:
            for step in astar_path:
                game_data["astar_current"] = step
                draw_compare_screen(screen, game_data)
                pygame.time.delay(300)
            steps = len(astar_path) - 1
            game_data["astar_result"] = f"A*: {steps} bước, {astar_duration}s, {astar_explored} nút."
        
        result_data["astar_done"] = True
    """ Hàm chạy thuật toán Greedy """
    def run_greedy():
        start_greedy = time.time()
        greedy_path, greedy_explored = greedy_best_first(greedy_board, return_explored=True)
        end_greedy = time.time()
        greedy_duration = round(end_greedy - start_greedy, 6)

        if greedy_path:
            for step in greedy_path:
                game_data["greedy_current"] = step
                draw_compare_screen(screen, game_data)
                pygame.time.delay(300)
            steps = len(greedy_path) - 1
            game_data["greedy_result"] = f"Greedy: {steps} bước, {greedy_duration}s, {greedy_explored} nút."
        
        result_data["greedy_done"] = True

    # --- Tạo 2 luồng ---
    astar_thread = threading.Thread(target=run_astar)
    greedy_thread = threading.Thread(target=run_greedy)

    astar_thread.start()
    greedy_thread.start()

    # --- Đợi cả 2 luồng kết thúc ---
    while not (result_data["astar_done"] and result_data["greedy_done"]):
        draw_compare_screen(screen, game_data)
        pygame.time.delay(100)

    # Đảm bảo kết thúc hoàn toàn
    astar_thread.join()
    greedy_thread.join()