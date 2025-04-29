import pygame
import time
from utils.button import Button
# Màu sắc
BG_COLOR = (40, 40, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)
pygame.font.init()
font_title = pygame.font.SysFont("Times New Roman", 48, bold=True)

easy = Button((390, 150, 200, 60), "EASY")
medium = Button((390, 230, 200, 60), "MEDIUM")
hard = Button((390, 310, 200, 60), "HARD")

""" Hàm vẽ màn hình mức độ """
def draw_level_screen(screen):
    screen.fill(BG_COLOR)
    title_surf = font_title.render("Please select your level of play!", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(title_surf, title_rect)

    for button in [easy, medium, hard]:
        button.check_hover(pygame.mouse.get_pos())
        button.draw(screen)

""" Hàm xử lý sự kiện tại các nút """
def handle_level_events(event, set_state, setup_game_func, game_data):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if easy.is_clicked(event.pos):
            game_data['size'] = 3
        elif medium.is_clicked(event.pos):
            game_data['size'] = 4
        elif hard.is_clicked(event.pos):
            game_data['size'] = 5
        else:
            return

        setup_game_func(game_data)
        set_state("play")

