from pieces import Bishop, Knight, Queen, Rook
import pygame
import sys
from board import Board
from minimax import minimax_AI
from time import sleep
import copy


"""
Author: Igor Kraszewski

File contains a class of the game

Methods of this class are responsible for the connection of all parts of the chess game
with the GUI made with pygame

"""


class Game():
    def __init__(self):
        pygame.init()
        pygame.time.delay(50)
        self.board = Board()
        self.name = 'Chess by Igor Kraszewski'
        self.width = 640
        self.one_box = self.width / 8
        self.window = pygame.display.set_mode(size=(self.width, self.width))
        pygame.display.set_caption(self.name)
        self.colors = {'creme': (255, 253, 208),
                       'brown': (233, 116, 81),
                       'black': (0, 0, 0),
                       'white': (255, 255, 255),
                       'light_grey': (211, 211, 211),
                       'red': (255, 0, 0),
                       'orange': (255, 69, 0),
                       'baby_blue': (137, 207, 240),
                       'purple': (192, 113, 254)}
        self.font = pygame.font.SysFont('Arial', 15)
        self.font_2 = pygame.font.SysFont('Arial', 50)
        self.image_size = 45
        self.img_box_point = (self.one_box - self.image_size) / 2
        self.history = [copy.deepcopy(self.board.board)]
        self.FEN_list = []

    # get index in board from mouse coordinates
    def piece_index(self, cords):
        x, y = cords
        row = int(y // self.one_box)
        column = int(x // self.one_box)
        return row, column

    def load_image(self, element):
        image = pygame.image.load(element).convert_alpha(self.window)
        return image

    # making possible moves for an individual piece highlighted on board
    def highlight(self, possible_moves):
        self.draw_board(possible_moves)
        pygame.display.update()

    # deleting the highlight from board
    def del_highlight(self):
        self.draw_board()
        pygame.display.update()

    # drawing a special type of board in situation when promotion occurs
    def promotion_board(self):
        color = self.board.turn
        middle = 3 * self.one_box
        queen_to_pick = Queen(-1, color, (3, 3))
        knight_to_pick = Knight(-1, color, (4, 3))
        bishop_to_pick = Bishop(-1, color, (4, 4))
        rook_to_pick = Rook(-1, color, (3, 4))
        pygame.draw.rect(self.window, self.colors['creme'],
                         pygame.Rect(middle, middle, 2 * self.one_box, 2 * self.one_box))
        self.window.blit(self.load_image(queen_to_pick.image),
                         (middle + self.img_box_point, middle + self.img_box_point))
        self.window.blit(self.load_image(rook_to_pick.image),
                         (middle + self.one_box + self.img_box_point, middle + self.img_box_point))
        self.window.blit(self.load_image(knight_to_pick.image),
                         (middle + self.img_box_point, middle + self.img_box_point + self.one_box))
        self.window.blit(self.load_image(bishop_to_pick.image),
                         (middle + self.one_box + self.img_box_point, middle + self.img_box_point + self.one_box))
        board_with_promo = copy.deepcopy(self.board.board)
        board_with_promo[3][3] = queen_to_pick
        board_with_promo[3][4] = rook_to_pick
        board_with_promo[4][3] = knight_to_pick
        board_with_promo[4][4] = bishop_to_pick
        pygame.display.update()

        return board_with_promo

    # calculating possible moves for a piece that was chosen
    def highlight_calc(self, cords):
        row, col = cords
        piece = self.board.board[row][col]
        possible_for_enemies = self.board.possible_for_enemies(self.board.turn)
        if piece.name == 'King':
            possible_for_enemies = self.board.possible_to_board(possible_for_enemies)
        possible_moves = piece.possible_moves(piece.pose, self.board.board,
                                              self.board.previous_state['board'],
                                              possible_for_enemies)
        possible_moves = self.board.legal_moves(possible_moves)

        return possible_for_enemies, possible_moves

    def draw_board(self, possible_moves=[], check=False, mate=False):
        king = self.board.w_king_pose if self.board.turn == "white" else self.board.b_king_pose
        sign = 7 * self.one_box + (13 / 16) * self.one_box
        self.window.fill(self.colors['white'])
        n = -1
        k = 0
        val = 1
        for i in range(1, 65):
            if i % 8 == 1 and i != 1:
                n = 0
                k += 1
                val = 0 if val else 1
            else:
                n += 1
            if i % 2 == val:
                pygame.draw.rect(self.window, self.colors['creme'],
                                 pygame.Rect(n * self.one_box, k * self.one_box,
                                             self.one_box, self.one_box))
            else:
                pygame.draw.rect(self.window, self.colors['brown'],
                                 pygame.Rect(n * self.one_box, k * self.one_box,
                                             self.one_box, self.one_box))
            if n == 7:
                self.window.blit(self.font.render(f'{8-k}', True, self.colors['black']),
                                 (sign, (1 / 8) * self.one_box + k * self.one_box))
            if k == 7:
                self.window.blit(self.font.render(f'{chr(ord("a") + n)}', True, self.colors['black']),
                                 ((1 / 8) * self.one_box + n * self.one_box, sign))
            if (k, n) == king:
                if check:
                    pygame.draw.rect(self.window, self.colors['orange'],
                                     pygame.Rect(n * self.one_box, k * self.one_box,
                                                 self.one_box, self.one_box))
                if check and mate:
                    pygame.draw.rect(self.window, self.colors['red'],
                                     pygame.Rect(n * self.one_box, k * self.one_box,
                                                 self.one_box, self.one_box))
            if type(self.board.board[k][n]) != str:
                self.window.blit(self.load_image(self.board.board[k][n].image),
                                 ((n * self.one_box + self.img_box_point),
                                  (k * self.one_box + self.img_box_point)))
        if len(possible_moves) > 0:
            for elem in possible_moves:
                if self.board.board[elem[1][0]][elem[1][1]] != "":
                    pygame.draw.circle(self.window, self.colors['purple'],
                                       (elem[1][1] * self.one_box + 40,
                                        elem[1][0] * self.one_box + 40), 20)
                else:
                    pygame.draw.circle(self.window, self.colors['baby_blue'],
                                       (elem[1][1] * self.one_box + 40,
                                        elem[1][0] * self.one_box + 40), 10)
        pygame.display.flip()

    # shows the replay of the game
    def replay(self, history):
        pygame.time.delay(100)
        for elem in history:
            cond = False
            self.board.board = elem
            self.draw_board()
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cond = True
                if cond:
                    break

    def play_vs_AI(self, depth):
        best_move = minimax_AI(self.board, self.board.previous_state['board'], depth,
                               float('-inf'), float('inf'),
                               True, self.board.turn)[0]
        self.board.move(best_move[0], best_move[1])
        return best_move

    # main function of game class which connects everything so that we can play chess
    def play(self, AI=False):
        FEN_cond = 0
        capture = False
        moved_piece = None
        picked = False
        promotion = False
        promo_piece = None
        self.draw_board()
        while True:
            pygame.time.delay(100)
            if FEN_cond == 0 and self.board.half_moves != 0:
                self.board.FEN_calculations(capture, moved_piece)
                FEN_cond = 1
                self.FEN_list.append(self.board.FEN[:-2].rstrip()[:-2].rstrip())
            if self.FEN_list.count(self.board.FEN[:-2].rstrip()[:-2].rstrip()) == 3:
                self.board.draw = True
            if self.board.draw or self.board.gameover:
                sleep(0.5)
                self.ending_screen()
            if AI and self.board.half_moves % 2 == 1:
                best_move = self.play_vs_AI(4)
                x, y = best_move[1]
                FEN_cond = 0
                self.history.append(copy.deepcopy(self.board.board))
                if type(self.board.previous_state['board'][x][y]) == str:
                    capture = False
                else:
                    capture = True
                self.draw_board(check=self.board.check, mate=self.board.gameover)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and not AI or \
                        event.type == pygame.MOUSEBUTTONDOWN and AI and self.board.half_moves % 2 == 0:
                    cords = pygame.mouse.get_pos()
                    row, col = self.piece_index(cords)
                    if not picked:
                        if type(self.board.board[row][col]) != str and \
                                self.board.board[row][col].color == self.board.turn:
                            possible_for_enemies, possible_moves = self.highlight_calc((row, col))
                            self.highlight(possible_moves)
                            picked = True
                            piece_cords = (row, col)
                    elif picked:
                        if (piece_cords, (row, col), False) in possible_moves or promotion:
                            if not promotion:
                                x, y = row, col
                            if self.board.board[piece_cords[0]][piece_cords[1]].name == "Pawn" and \
                                    (x == 7 or x == 0) or promotion:
                                promotion = True
                                promo_board = self.promotion_board()
                                if (row == 3 or row == 4) and (col == 3 or col == 4):
                                    promo_piece = promo_board[row][col]
                                    promo_piece.pose = (x, y)
                                    promotion = False
                            if not promotion:
                                moved_piece = self.board.board[piece_cords[0]][piece_cords[1]]
                                self.board.move(piece_cords, (x, y), promo_piece)
                                promo_piece = None
                                FEN_cond = 0
                                self.history.append(copy.deepcopy(self.board.board))
                                if type(self.board.previous_state['board'][x][y]) == str:
                                    capture = False
                                else:
                                    capture = True
                                moves_to_draw = self.board.FEN[:-2].rstrip()
                                if int(moves_to_draw[-2:] == 50):
                                    self.board.draw = True
                                picked = False
                                self.draw_board(check=self.board.check, mate=self.board.gameover)
                        elif type(self.board.board[row][col]) != str and not promotion and \
                                self.board.board[row][col].color == self.board.turn:
                            self.del_highlight()
                            possible_for_enemies, possible_moves = self.highlight_calc((row, col))
                            self.highlight(possible_moves)
                            piece_cords = row, col
                            picked = True
            if True in (self.board.gameover, self.board.draw):
                break

    # function which calculates what choice player made in the menu
    def pick_menu_option(self, end=False):
        left_button = False
        right_button = False
        replay = False
        while True:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cords = pygame.mouse.get_pos()
                    width, height = cords
                    if self.one_box < width < 3.9 * self.one_box and \
                            3 * self.one_box < height < 5 * self.one_box:
                        left_button = True
                    elif 4.1 * self.one_box < width < 7 * self.one_box and \
                            3 * self.one_box < height < 5 * self.one_box:
                        right_button = True
                    elif 3.5 * self.one_box < width < 4.5 * self.one_box and \
                            2.25 * self.one_box < height < 2.75 * self.one_box and \
                            end:
                        replay = True
            if True in (left_button, right_button, replay):
                return left_button, right_button, replay

    # drawing starting menu on the board
    def menu(self):
        self.draw_board()
        pygame.draw.rect(self.window, self.colors['white'],
                         pygame.Rect(self.one_box, 3 * self.one_box, 2.9 * self.one_box, 2 * self.one_box))
        pygame.draw.rect(self.window, self.colors['white'],
                         pygame.Rect(4.1 * self.one_box, 3 * self.one_box, 2.9 * self.one_box, 2 * self.one_box))
        self.window.blit(self.load_image('images/friend.png'),
                         ((self.one_box),
                          (3 * self.one_box)))
        self.window.blit(self.load_image('images/AI.png'),
                         ((4.1 * self.one_box),
                          (3 * self.one_box)))
        pygame.display.update()

    # drawing an ending screen on the board
    def ending_screen(self):
        pygame.draw.rect(self.window, self.colors['white'],
                         pygame.Rect(self.one_box, 3 * self.one_box, 2.9 * self.one_box, 2 * self.one_box))
        pygame.draw.rect(self.window, self.colors['white'],
                         pygame.Rect(4.1 * self.one_box, 3 * self.one_box, 2.9 * self.one_box, 2 * self.one_box))
        pygame.draw.rect(self.window, self.colors['white'],
                         pygame.Rect(3.5 * self.one_box, 2.25 * self.one_box, self.one_box, 0.5 * self.one_box))
        self.window.blit(self.load_image('images/one_more.png'),
                         ((self.one_box),
                          (3 * self.one_box)))
        self.window.blit(self.load_image('images/end.png'),
                         ((4.1 * self.one_box),
                          (3 * self.one_box)))
        self.window.blit(self.load_image('images/replay.png'),
                         ((3.5 * self.one_box),
                          (2.25 * self.one_box)))
        pygame.display.update()
