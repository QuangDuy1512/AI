import pygame
pygame.init() 
BG_COLOR = (40, 40, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)

font_button = pygame.font.SysFont("Times New Roman", 32, bold=True)    # Font cho nút
font_title = pygame.font.SysFont("Times New Roman", 48, bold=True)     # Font tiêu đề lớn
font_note = pygame.font.SysFont("Times New Roman", 24)                 # Font ghi chú nhỏ

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=12)

        text_surf = font_button.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

