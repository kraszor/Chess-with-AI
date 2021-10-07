from pieces import Pawn, Knight, King, Queen, Rook, Bishop
from copy import deepcopy


"""
Author: Igor Kraszewski

File contains a class of the chess board

Object of this class is used in the class of the game,
also it contains important informations about the current state on the board

"""


class Board():
    def __init__(self):
        self.w_king_pose = (7, 4)
        self.b_king_pose = (0, 4)
        self.turn = "white"
        self.gameover = False
        self.draw = False
        self.check = False
        self.board = self.starting_board()
        self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.half_moves = 0
        self.half_moves_no_pawn_no_capture = 0
        self.made_moves = []
        self.previous_state = {'board': deepcopy(self.board),
                               'w_king': self.w_king_pose,
                               'b_king': self.b_king_pose,
                               'turn': self.turn,
                               'FEN': self.FEN,
                               'half_moves': self.half_moves}

    # creating a starting board which contains objects of the individual pieces classes
    def starting_board(self):
        wp1 = Pawn(1, "white", (6, 0))
        wp2 = Pawn(2, "white", (6, 1))
        wp3 = Pawn(3, "white", (6, 2))
        wp4 = Pawn(4, "white", (6, 3))
        wp5 = Pawn(5, "white", (6, 4))
        wp6 = Pawn(6, "white", (6, 5))
        wp7 = Pawn(7, "white", (6, 6))
        wp8 = Pawn(8, "white", (6, 7))
        bp1 = Pawn(9, "black", (1, 0))
        bp2 = Pawn(10, "black", (1, 1))
        bp3 = Pawn(11, "black", (1, 2))
        bp4 = Pawn(12, "black", (1, 3))
        bp5 = Pawn(13, "black", (1, 4))
        bp6 = Pawn(14, "black", (1, 5))
        bp7 = Pawn(15, "black", (1, 6))
        bp8 = Pawn(16, "black", (1, 7))
        wr1 = Rook(17, "white", (7, 0))
        wr2 = Rook(18, "white", (7, 7))
        br1 = Rook(19, "black", (0, 0))
        br2 = Rook(20, "black", (0, 7))
        wb1 = Bishop(21, "white", (7, 2))
        wb2 = Bishop(22, "white", (7, 5))
        bb1 = Bishop(23, "black", (0, 2))
        bb2 = Bishop(24, "black", (0, 5))
        wn1 = Knight(25, "white", (7, 1))
        wn2 = Knight(26, "white", (7, 6))
        bn1 = Knight(27, "black", (0, 1))
        bn2 = Knight(28, "black", (0, 6))
        wq = Queen(29, "white", (7, 3))
        bq = Queen(29, "black", (0, 3))
        wk = King(100, "white", (7, 4))
        bk = King(101, "black", (0, 4))

        starting_board = [[br1, bn1, bb1, bq, bk, bb2, bn2, br2],
                          [bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          [wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8],
                          [wr1, wn1, wb1, wq, wk, wb2, wn2, wr2]]

        return starting_board

    # calculating all possible moves for the enemy
    def possible_for_enemies(self, color):
        enemy_possibilities = []
        for elem in self.board:
            for i in elem:
                if type(i) != str:
                    if i.color != color:
                        possible_for_enemy = i.possible_moves(i.pose,
                                                              self.board)
                        enemy_possibilities += possible_for_enemy

        return enemy_possibilities

    # changing possible moves from the list to the board with marked points
    def possible_to_board(self, possible):
        possible_board = [["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""],
                          ["", "", "", "", "", "", "", ""]]
        for elem in possible:
            space_1 = possible_board[elem[0][0]][elem[0][1]]
            space_2 = possible_board[elem[1][0]][elem[1][1]]
            if space_1 == "":
                possible_board[elem[0][0]][elem[0][1]] = self.board[elem[0][0]][elem[0][1]]
                possible_board[elem[0][0]][elem[0][1]].status = False
            if type(space_2) != str:
                possible_board[elem[1][0]][elem[1][1]].status = True
            else:
                possible_board[elem[1][0]][elem[1][1]] = 'x'

        return possible_board

    # calculating all possible moves for the ally
    def possible_for_allies(self, possible_for_enemy, isAI):
        ally_possibilities = []
        for elem in self.board:
            for i in elem:
                if type(i) != str and \
                   i.color == self.turn:
                    if i.name == "King" and len(possible_for_enemy) > 0 and \
                            len(possible_for_enemy) != 8 and len(possible_for_enemy[0]) != 8:
                        possible_for_enemy = self.possible_to_board(possible_for_enemy)
                    possible_for_ally = \
                        i.possible_moves(i.pose,
                                         self.board,
                                         possible_for_enemy=possible_for_enemy)
                    if len(possible_for_ally) == 0:
                        continue
                    possible_for_ally = self.legal_moves(possible_for_ally)
                    if len(possible_for_ally) > 0 and not isAI:
                        return possible_for_ally
                    ally_possibilities += possible_for_ally

        return list(set(ally_possibilities))

    # calculating diffrence in points which is used for the AI
    def points_diff(self, color):
        if self.gameover:
            return float('inf')
        white_points = 0
        black_points = 0
        for row in self.board:
            for elem in row:
                if type(elem) != str:
                    if elem.color == "black":
                        black_points += elem.points
                    else:
                        white_points += elem.points
        if color == "white":
            points_diff = white_points - black_points
        else:
            points_diff = black_points - white_points

        return points_diff

    # reset status of every piece on the board
    def board_status_reset(self):
        for row in self.board:
            for elem in row:
                if type(elem) != str:
                    elem.status = False

    # recalculating possible moves to only those which are legal in terms of the chess rules
    def legal_moves(self, possible_for_ally):
        illegal_moves = []
        if self.turn == "white":
            king_pose = self.w_king_pose
            x, y = king_pose
            king = self.board[x][y]
        elif self.turn == "black":
            king_pose = self.b_king_pose
            x, y = king_pose
            king = self.board[x][y]
        p_test = Pawn(1000, self.turn, (10, 10))
        for elem in possible_for_ally:
            x, y = king_pose
            if elem[2] is True:
                continue
            else:
                if elem[0] == (x, y):
                    p_test = king
                    x, y = elem[1]
                piece = self.board[elem[0][0]][elem[0][1]]
                picked = self.board[elem[1][0]][elem[1][1]]
                self.board[elem[1][0]][elem[1][1]] = p_test
                self.board[elem[0][0]][elem[0][1]] = ""
                enemy_possible = self.possible_for_enemies(self.turn)
                if p_test == king:
                    self.board[elem[0][0]][elem[0][1]] = ""
                    self.board[elem[1][0]][elem[1][1]] = ""
                    additional_possiblities = self.possible_for_enemies(self.turn)
                    self.board[elem[1][0]][elem[1][1]] = p_test
                    enemy_possible = list(set(enemy_possible + additional_possiblities))
                for item in enemy_possible:
                    pawn_cond = abs(item[1][0] - item[0][0]) == 1 and \
                               item[1][1] == item[0][1] and self.board[item[0][0]][item[0][1]].name == "Pawn"
                    if item[1] == (x, y) and item[2] is False and not pawn_cond:
                        illegal_moves.append(elem)
                self.board[elem[0][0]][elem[0][1]] = piece
                self.board[elem[1][0]][elem[1][1]] = picked
        legal_moves = list(set(possible_for_ally) - set(illegal_moves))

        return legal_moves

    # calulating FEN code
    def FEN_calculations(self, capture, piece):
        FEN = ""
        cords = ()
        for a, row in enumerate(self.board):
            empty_spaces = 0
            for b, elem in enumerate(row):
                if type(elem) != str:
                    if empty_spaces != 0:
                        FEN += str(empty_spaces)
                        empty_spaces = 0
                    if elem.name == "Pawn" and elem.color == self.turn:
                        if elem.en_passant != ():
                            cords = elem.en_passant
                    if elem.color == "black":
                        FEN += elem.symbol.lower()
                        if elem.symbol == "K":
                            elem.possible_moves(elem.pose, self.board)
                            black_castle = self.board[a][b].castle
                    else:
                        FEN += elem.symbol
                        if elem.symbol == "K":
                            elem.possible_moves(elem.pose, self.board)
                            white_castle = self.board[a][b].castle
                else:
                    empty_spaces += 1
            if empty_spaces != 0:
                FEN += str(empty_spaces)
            FEN += "/"
            b = -1
        if self.turn == "white":
            turn = "w"
        else:
            turn = "b"
        if cords != ():
            space_symbol = chr(ord("a") + cords[1]) + str(8 - cords[0])
        else:
            space_symbol = "-"
        moves = self.half_moves // 2 + 1
        if piece.name == "Pawn" or capture:
            self.half_moves_no_pawn_no_capture = 0
        else:
            self.half_moves_no_pawn_no_capture = self.half_moves_no_pawn_no_capture + 1
        if white_castle == "" and black_castle == "":
            black_castle = "-"
        FEN = FEN[:-1]
        FEN = FEN + f' {turn} {white_castle}{black_castle} {space_symbol} {self.half_moves_no_pawn_no_capture} {moves}'
        self.FEN = FEN

    # memorizing previous state of the chess board
    def set_prev_state(self):
        self.previous_state = {
                               'board': deepcopy(self.board),
                               'w_king': self.w_king_pose,
                               'b_king': self.b_king_pose,
                               'turn': self.turn,
                               'FEN': self.FEN,
                               'half_moves': self.half_moves}

    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    # calculating current state on the board - is it game over or not?
    def calc_game_status(self, possible_for_enemy, possible_for_ally):
        checkmate = False
        stalemate = False
        king = self.w_king_pose if self.turn == "white" else self.b_king_pose
        check = self.board[king[0]][king[1]].check_status(possible_for_enemy)
        if check:
            checkmate = self.board[king[0]][king[1]].checkmate_status(check, possible_for_ally)
        else:
            stalemate = self.board[king[0]][king[1]].stalemate(check, possible_for_ally)
        self.check = check
        self.gameover = checkmate
        self.draw = stalemate

        return check, checkmate, stalemate

    # making move which also sets new previous state and changes the turn
    def move(self, current_pose, picked_pose, promo=None):
        enemy = "black" if self.turn == "white" else "white"
        self.set_prev_state()
        self.made_moves.append(deepcopy(self.previous_state))
        moving_piece = self.board[current_pose[0]][current_pose[1]]
        moving_piece.first_move = False
        if moving_piece.name == "King" and \
           (picked_pose[1] + 2 == current_pose[1]
                or picked_pose[1] - 2 == current_pose[1]):
            self.board[picked_pose[0]][picked_pose[1]] = moving_piece
            self.board[current_pose[0]][current_pose[1]] = ""
            if picked_pose[1] == 6:
                self.board[picked_pose[0]][picked_pose[1] + 1].pose = \
                    (current_pose[0], current_pose[1] + 1)
                self.board[current_pose[0]][current_pose[1] + 1] = \
                    self.board[picked_pose[0]][picked_pose[1] + 1]
                self.board[picked_pose[0]][picked_pose[1] + 1] = ""
            elif picked_pose[1] == 2:
                self.board[picked_pose[0]][picked_pose[1] - 2].pose = \
                    (current_pose[0], current_pose[1] - 1)
                self.board[current_pose[0]][current_pose[1] - 1] = \
                    self.board[picked_pose[0]][picked_pose[1] - 2]
                self.board[picked_pose[0]][picked_pose[1] - 2] = ""
        elif moving_piece.name == "Pawn" and \
            self.board[picked_pose[0]][picked_pose[1]] == "" and \
                (picked_pose[1] + 1 == current_pose[1] or
                    picked_pose[1] - 1 == current_pose[1]):
            self.board[picked_pose[0]][picked_pose[1]] = moving_piece
            self.board[current_pose[0]][current_pose[1]] = ""
            if self.board[picked_pose[0] + 1][picked_pose[1]] == "":
                self.board[picked_pose[0] - 1][picked_pose[1]] = ""
            elif self.board[picked_pose[0] - 1][picked_pose[1]] == "":
                self.board[picked_pose[0] + 1][picked_pose[1]] = ""
        else:
            if promo is not None:
                moving_piece = promo
            self.board[picked_pose[0]][picked_pose[1]] = moving_piece
            self.board[current_pose[0]][current_pose[1]] = ""
        moving_piece.move(picked_pose)
        if moving_piece.name == 'King':
            if moving_piece.color == 'white':
                self.w_king_pose = picked_pose
            else:
                self.b_king_pose = picked_pose
        self.half_moves += 1
        self.switch_turn()
        self.board_status_reset()
        possible_for_enemy = self.possible_for_enemies(enemy)
        possible_for_enemy = self.possible_to_board(possible_for_enemy)
        possible_for_ally = self.possible_for_allies(possible_for_enemy, False)
        self.calc_game_status(possible_for_enemy, possible_for_ally)

    # sets the board state to this before the move was made
    def undo_move(self):
        self.previous_state = self.made_moves.pop()
        self.board = self.previous_state['board']
        self.b_king_pose = self.previous_state['b_king']
        self.w_king_pose = self.previous_state['w_king']
        self.turn = self.previous_state['turn']
        self.half_moves = self.previous_state['half_moves']
        self.FEN = self.previous_state['FEN']
        self.previous_state = self.made_moves[-1]
