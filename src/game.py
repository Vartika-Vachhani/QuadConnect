import pygame
import sys
from enum import Enum
from variables import ROW_COUNT, COLUMN_COUNT, SQUARESIZE, size, RADIUS, colors, height, width, PLAYER, AI, \
    PLAYER_PIECE, AI_PIECE, thinking_time, game_end_button_width, game_end_button_height, level_button_height, \
    level_button_width
from functions import create_board, is_valid_location, get_next_open_row, drop_piece, game_over_check, draw_board, \
    board, screen, draw_dotted_circle
from score_ai import pick_best_move
from minmax_ai import minimax
from ui_components import Button
from ui_components import ai_move_sound, self_move_sound, ai_wins_sound, player_wins_sound
import time
from playervsplayer import ConnectFourPvP  # Importing Player vs. Player module
from playervsai import QuadConnectGame
from debug import *

class GameMode(Enum):
    PvP = 1
    PvAI = 2

class QuadConnectHome:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("QuadConnect")
        self.font = pygame.font.SysFont(None, 48)
        self.selected_mode = None
        self.pvp_button = Button(colors["GREEN"], width // 2 - 150, height // 2 - 50, 300, 80, 'Multi Player')
        self.pvai_button = Button(colors["RED"], width // 2 - 150, height // 2 + 50, 300, 80, 'AI')

        # Added content
        self.project_info_font = pygame.font.SysFont(None, 24)
        self.designer1_text = self.project_info_font.render("ARTIFICIAL INTELLIGENCE PROJECT", True, colors["YELLOW"])
        self.designer2_text = self.project_info_font.render("Designed by: VARTIKA VACHHANI (Sem 6)", True, colors["YELLOW"])
        self.designer3_text = self.project_info_font.render("                          VIVEK PATEL (Sem 6)", True, colors["YELLOW"])

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    def draw_buttons(self):
        self.pvp_button.draw(screen)
        self.pvai_button.draw(screen)

    def draw_project_info(self):
        screen.blit(self.designer1_text, (10, height - 80))
        screen.blit(self.designer2_text, (10, height - 50))
        screen.blit(self.designer3_text, (10, height - 20))

    def check_button_click(self, pos):
        if self.pvp_button.is_over(pos):
            self.selected_mode = GameMode.PvP
        elif self.pvai_button.is_over(pos):
            self.selected_mode = GameMode.PvAI

    def run(self):
        start_time = time.time()
        print(start_time)
        while True:
            debug(start_time)
            screen.fill(colors["GREY"])
            self.draw_text("QuadConnect", self.font, colors["YELLOW"], width // 2, 100)
            self.draw_buttons()
            self.draw_project_info()  # Display project info
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_button_click(pygame.mouse.get_pos())
                    if self.selected_mode:
                        return self.selected_mode
            self.clock.tick(30)

if __name__ == "__main__":
    home = QuadConnectHome()
    selected_mode = home.run()
    if selected_mode == GameMode.PvP:
        game_pvp = ConnectFourPvP()
        game_pvp.run()
    elif selected_mode == GameMode.PvAI:
        game_pvai = QuadConnectGame()
        game_pvai.game_start()
