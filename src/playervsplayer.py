import pygame
import sys
import math
import random
import time

from enum import Enum
from variables import ROW_COUNT, COLUMN_COUNT, SQUARESIZE, size, RADIUS, colors, height, width, PLAYER, AI, \
    PLAYER_PIECE, AI_PIECE, thinking_time, game_end_button_width, game_end_button_height, level_button_height, \
    level_button_width, PLAYER_TWO, PLAYER_TWO_PIECE
from functions import create_board, is_valid_location, get_next_open_row, drop_piece, game_over_check, draw_board, \
    board, screen, draw_dotted_circle
from score_ai import pick_best_move
from minmax_ai import minimax
from ui_components import Button
from ui_components import ai_move_sound, self_move_sound, ai_wins_sound, player_wins_sound
from ui_components import p1_move_sound, p2_move_sound, p1_wins_sound, p2_wins_sound

class ConnectFourPvP:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() #added to initialize sound
        self.game_over = False
        self.turn = random.randint(PLAYER, AI)
        self.board = create_board()
        self.myfont = pygame.font.SysFont("monospace", 80)
        self.small_font = pygame.font.SysFont("monospace", 30)
        padding = 20
        restart_button_y = height // 2
        quit_button_y = restart_button_y + game_end_button_height + padding
        self.center_x = width // 2 - game_end_button_width // 2
        self.quit_button = Button(colors["RED"], self.center_x, quit_button_y, game_end_button_width,
                                  game_end_button_height, 'Quit')
        self.restart_button = Button(colors["GREEN"], self.center_x, restart_button_y,
                                     game_end_button_width, game_end_button_height,
                                     'Restart')
        pygame.display.set_caption("QuadConnect")
        screen.fill(colors["DARKGREY"])
        draw_board(self.board)
        self.latest_timestamp = 0
        self.pieces_placed = 0  # Track the number of pieces placed
        self.timer = 180  # 3 minutes timer (3 minutes * 60 seconds)
        pygame.display.update()
        

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    def handle_mouse_motion(self, event):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))
        posx = event.pos[0]
        if self.turn == PLAYER:
            draw_dotted_circle(screen, posx, int(SQUARESIZE / 2), RADIUS, colors["YELLOW"], gap_length=6)
        pygame.display.update()

    def handle_mouse_button_down(self, event):
        self.latest_timestamp = pygame.time.get_ticks() // 1000  # Convert milliseconds to seconds
        self.draw_text(str(self.latest_timestamp), self.myfont, colors["YELLOW"], 100, 30)
        # print("clicked")
        posx = event.pos[0]
        col = int(posx / SQUARESIZE)
        if is_valid_location(self.board, col):
            self.drop_piece_and_check_win(col)
            self.latest_timestamp = 0  # Reset the timestamp
            self.pieces_placed += 1
            
            # if self.pieces_placed == 2:  # Check if two pieces are placed
                # 
            if self.game_over:
                self.handle_game_over()

    def drop_piece_and_check_win(self, col):
        row = get_next_open_row(self.board, col)
        if self.turn == PLAYER:
            piece_color = colors["GREEN"]
            p2_move_sound.play()
            piece = PLAYER_PIECE
            next_turn = PLAYER_TWO
        else:
            piece_color = colors["RED"]
            p1_move_sound.play()
            piece = PLAYER_TWO_PIECE
            next_turn = PLAYER
        drop_piece(self.board, row, col, piece)
        self.draw_piece(row, col, piece_color)
        if game_over_check(self.board, piece):
            self.game_over = True
            self.display_winner()
        else:
            self.turn = next_turn

    def handle_game_over(self):
        self.restart_button.draw(screen, outline_color=colors["DARKGREY"])
        self.quit_button.draw(screen, outline_color=colors["DARKGREY"])  # Draw the quit button
        pygame.display.update()
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.latest_timestamp = pygame.time.get_ticks() // 1000  # Convert milliseconds to seconds
                    self.draw_text(str(self.latest_timestamp), self.myfont, colors["YELLOW"], width // 2, 100)
                    print("clicked")
                    posx, posy = event.pos
                    if self.quit_button.is_over((posx, posy)):
                        pygame.quit()  # Quit the game
                        sys.exit()
                    elif self.restart_button.is_over((posx, posy)):
                        self.__init__()  # Restart the game
                        self.game_over = False  # Reset game over flag
                        return
            pygame.display.update()

    def display_winner(self):
        if self.turn == PLAYER:
            message = "Player 1 wins!"
            p1_wins_sound.play()
        else:
            message = "Player 2 wins!"
            p2_wins_sound.play()
        label = self.myfont.render(message, 1, colors["RED"])
        screen.blit(label, (40, 10))
        pygame.display.update()

    def draw_piece(self, row, col, color):
        pygame.draw.circle(screen, color, (int(col * SQUARESIZE + SQUARESIZE / 2), height - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()  # Create a clock object to control the frame rate
        while not self.game_over:
            clock.tick(60)  # Limit the frame rate to 60 frames per second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
            # Update the timer
            self.timer -= 1
            if self.timer < 0:
                self.timer = 0
            # Draw the timer
            self.draw_text("Timer: {}:{}".format(self.timer // 60, self.timer % 60), self.small_font, colors["YELLOW"], width - 100, 30)

if __name__ == "__main__":
    game = ConnectFourPvP()
    game.run()
