import pygame
import sys
import math
import random
import time

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

class Difficulty(Enum):
    EASY = 1
    INTERMEDIATE = 2
    HARD = 3

class QuadConnectGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() #added to initialize sound
        self.game_over = False
        self.turn = random.randint(PLAYER, AI)
        self.board = create_board()
        self.myfont = pygame.font.SysFont("monospace", 80)
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
        self.difficulty = self.choose_difficulty()
        screen.fill(colors["DARKGREY"])
        draw_board(self.board)
        pygame.display.update()

    def handle_mouse_motion(self, event):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))
        posx = event.pos[0]
        if self.turn == PLAYER:
            draw_dotted_circle(screen, posx, int(SQUARESIZE / 2), RADIUS, colors["YELLOW"], gap_length=6)
        pygame.display.update()

    def handle_mouse_button_down(self, event):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))
        posx = event.pos[0]
        if self.turn == PLAYER:
            col = int(math.floor(posx / SQUARESIZE))
            if is_valid_location(self.board, col):
                self_move_sound.play()
                self.drop_piece_and_check_win(col, PLAYER_PIECE, "You win!! ^_^")
                self.turn = AI
                self.render_thinking("Thinking...")
                draw_board(self.board)
        if self.game_over:
            if self.quit_button.is_over((posx, event.pos[1])):
                sys.exit()
            elif self.restart_button.is_over((posx, event.pos[1])):
                self.__init__()

    def ai_move(self):
        thinking_time = 1
        if self.difficulty == Difficulty.EASY:
            col = random.randint(0, COLUMN_COUNT-1)
            time.sleep(thinking_time + 1)
        if self.difficulty == Difficulty.INTERMEDIATE:
            col = pick_best_move(self.board,
                                AI_PIECE,
                                directions=tuple(1 if i in random.sample(range(4), 2) else 0 for i in range(4)))
            time.sleep(thinking_time + 1.2)
        if self.difficulty == Difficulty.HARD:
            col = pick_best_move(self.board, AI_PIECE)
            time.sleep(thinking_time + 1.5)

        if is_valid_location(self.board, col):
            ai_move_sound.play()
            self.drop_piece_and_check_win(col, AI_PIECE, "AI wins!! :[")
            self.turn = PLAYER

    def drop_piece_and_check_win(self, col, piece, win_message):
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, piece)
        draw_board(self.board)
        pygame.display.update()
        if game_over_check(self.board, piece):
            self.display_winner(win_message)
            print(win_message) 
            self.game_over = True
            return self.handle_game_over()

    def display_winner(self, message):
        if self.turn == PLAYER:
            print("playerwinconsole")
            message = "You win!! ^_^"
            color = colors["GREEN"]
            player_wins_sound.play()
        else:
            color = colors["RED"]
            print("aiwinconsole")
            message = "AI wins!! :["
            ai_wins_sound.play()
        label = self.myfont.render(message, 1, color)
        screen.blit(label, (40, 10))
        pygame.display.update()

    def handle_game_over(self):
        self.clear_label()
        draw_board(self.board)
        self.quit_button.draw(screen, outline_color=colors["DARKGREY"])
        self.restart_button.draw(screen, outline_color=colors["DARKGREY"])
        pygame.display.update()
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.quit_button.is_over((posx, posy)):
                        sys.exit()
                    elif self.restart_button.is_over((posx, posy)):
                        self.__init__()
                        return self.game_start()

            pygame.display.update()

    def choose_difficulty(self):
        btn_height = 90
        text_color = colors['DARKGREY']
        btn_y = [i * (btn_height + 20) + height/1.8 for i in range(-3,3)]
        self.easy = Button(colors['GREEN'], self.center_x,
                           btn_y[1], 250, btn_height,
                           'EASY',
                           text_color=text_color)
        self.intermediate = Button(colors['YELLOW'], self.center_x,
                            btn_y[3], 250, btn_height,
                            'INTERMEDIATE',
                            text_color=text_color)

        self.hard = Button(colors['RED'], self.center_x,
                           btn_y[5], 250, btn_height,
                           'HARD',
                           text_color=text_color)


        screen.fill(colors['GREY'])
        self.easy.draw(screen)
        self.intermediate.draw(screen)
        self.hard.draw(screen)


        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.easy.is_over((posx, posy)):
                        return Difficulty.EASY
                    elif self.intermediate.is_over((posx, posy)):
                        return Difficulty.INTERMEDIATE
                    elif self.hard.is_over((posx, posy)):
                        return Difficulty.HARD

    def game_start(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
            if self.turn == AI and not self.game_over:
                self.ai_move()
            if self.game_over:
                self.handle_game_over()

            pygame.display.update()

    def clear_label(self):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))


    def render_thinking(self, text):
        self.clear_label()
        label = pygame.font.SysFont("monospace", 60).render(text, 1, colors["YELLOW"])
        screen.blit(label, (40, 10))
        pygame.display.update()

if __name__ == "__main__":
    game = QuadConnectGame()
    game.game_start()
