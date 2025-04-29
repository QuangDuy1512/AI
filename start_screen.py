
import pygame
import time
from utils.button import Button
from puzzle import PuzzleBoard
from A_star import a_star
from puzzle import PuzzleBoard

# Màu sắc
BG_COLOR = (40, 40, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)

# Font chữ
pygame.font.init()
font_button = pygame.font.SysFont("Times New Roman", 32, bold=True)    # Font cho nút
font_title = pygame.font.SysFont("Times New Roman", 48, bold=True)     # Font tiêu đề lớn
font_note = pygame.font.SysFont("Times New Roman", 24)                 # Font ghi chú nhỏ

start_button = Button((390, 200, 220, 60), "START")
compare_btn = Button((390, 270, 220, 60), "COMPARE AI")
exit_btn = Button((390, 340, 220, 60), "EXIT")

""" Hàm vẽ màn hình bắt đầu """
def draw_start_screen(screen):
    screen.fill(BG_COLOR)

    title_surf = font_title.render("Welcome to Jigsaw Puzzle Game!", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 120))
    screen.blit(title_surf, title_rect)

    for button in [start_button, compare_btn, exit_btn]:
        button.check_hover(pygame.mouse.get_pos())
        button.draw(screen)

    note_surf = font_note.render("Group_1 - AI", True, TEXT_COLOR)
    note_rect = note_surf.get_rect(center=(screen.get_width() // 2, 450))
    screen.blit(note_surf, note_rect)
    note_surf = font_note.render("Ho Chi Minh city University of Technology and Education", True, TEXT_COLOR)
    note_rect = note_surf.get_rect(center=(screen.get_width() // 2, 475))
    screen.blit(note_surf, note_rect)

    # Đưa ảnh lên giao diện
    image1 = pygame.image.load("Image/assistant.png")
    image1 = pygame.transform.scale(image1, (200, 200))  # kích thước mới (rộng x cao)
    screen.blit(image1, (750, 250))  
    image2 = pygame.image.load("Image/jigsaw.png")
    image2 = pygame.transform.scale(image2, (200, 200))  
    screen.blit(image2, (70, 250)) 

""" Hàm xử lý sự kiện """
def handle_start_events(event, on_start, on_compare):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.is_clicked(event.pos):
            on_start()
        elif compare_btn.is_clicked(event.pos):
            on_compare()
        elif exit_btn.is_clicked(event.pos):   
            pygame.quit()
            exit()
        
