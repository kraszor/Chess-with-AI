from abc import ABC, abstractmethod


"""
Author: Igor Kraszewski

File contains abstract class of a Piece and inheriting classes of invidual pieces

Objects of this classes are used in board and game classes

"""


class Piece(ABC):

    def __init__(self, id, color, pose, first_move, status):
        self.id = id
        self.color = color
        self.pose = pose
        self.first_move = first_move
        self.status = status

    def move(self, picked_pose):
        self.pose = picked_pose

    @abstractmethod
    def possible_moves(self):
        pass


class Pawn(Piece):

    def __init__(self, id, color,
                 pose, first_move=True,
                 status=False, en_passant=()):
        super().__init__(id, color, pose, first_move, status)
        self.name = "Pawn"
        self.symbol = "P"
        self.points = 10
        if color == "black":
            image = "images/b_pawn.png"
        else:
            image = "images/w_pawn.png"
        self.image = image
        self.en_passant = en_passant

    def possible_moves(self,
                       current_pose,
                       current_board,
                       prevboard=[[]],
                       possible_for_enemy=[[]]):
        possible_moves = []
        if self.color == "white":
            if current_pose[0] == 6:
                if current_board[current_pose[0] - 1][current_pose[1]] == "" and \
                        current_board[current_pose[0] - 2][current_pose[1]] == "":
                    possible_moves.append((current_pose,
                                          (current_pose[0] - 2,
                                           current_pose[1]), False))
            if current_board[current_pose[0] - 1][current_pose[1]] == "":
                possible_moves.append((current_pose,
                                      (current_pose[0] - 1,
                                       current_pose[1]), False))

            try:
                if current_board[current_pose[0] - 1][current_pose[1] + 1].color == "black":
                    possible_moves.insert(0, (current_pose,
                                              (current_pose[0] - 1,
                                               current_pose[1] + 1), False))
                if current_board[current_pose[0] - 1][current_pose[1] + 1].color == "white":
                    current_board[current_pose[0] - 1][current_pose[1] + 1].status = True
            except Exception:
                pass

            try:
                if current_board[current_pose[0] - 1][current_pose[1] - 1].color == "black":
                    possible_moves.insert(0, (current_pose,
                                              (current_pose[0] - 1,
                                               current_pose[1] - 1), False))
                if current_board[current_pose[0] - 1][current_pose[1] - 1].color == "White":
                    current_board[current_pose[0] - 1][current_pose[1] - 1].status = True
            except Exception:
                pass

            # en passant for white
            if current_pose[0] == 3:
                try:
                    if current_board[3][current_pose[1] + 1].color == "black" and \
                       current_board[3][current_pose[1] + 1].name == "Pawn" and \
                       prevboard[1][current_pose[1] + 1].id == current_board[3][current_pose[1] + 1].id:
                        possible_moves.insert(0, (current_pose,
                                                  (2, current_pose[1] + 1),
                                                  False))
                        self.en_passant = (2, current_pose[1] + 1)
                except Exception:
                    pass

                try:
                    if current_board[3][current_pose[1] - 1].color == "black" and \
                       current_board[3][current_pose[1] - 1].name == "Pawn" and \
                       prevboard[1][current_pose[1] - 1].id == current_board[3][current_pose[1] - 1].id:
                        possible_moves.insert(0, (current_pose,
                                                  (2, current_pose[1] - 1),
                                                  False))
                        self.en_passant = (2, current_pose[1] - 1)
                except Exception:
                    pass

        if self.color == "black":
            if current_pose[0] == 1:
                if current_board[current_pose[0] + 1][current_pose[1]] == \
                        "" and current_board[current_pose[0] + 2][current_pose[1]] == "":
                    possible_moves.append((current_pose,
                                           (current_pose[0] + 2,
                                            current_pose[1]), False))
            if current_board[current_pose[0] + 1][current_pose[1]] == "":
                possible_moves.append((current_pose,
                                       (current_pose[0] + 1,
                                        current_pose[1]), False))

            try:
                if current_board[current_pose[0] + 1][current_pose[1] + 1].color == "white":
                    possible_moves.insert(0, (current_pose,
                                              (current_pose[0] + 1,
                                               current_pose[1] + 1), False))
                if current_board[current_pose[0] + 1][current_pose[1] + 1].color == "black":
                    current_board[current_pose[0] + 1][current_pose[1] + 1].status = True
            except Exception:
                pass

            try:
                if current_board[current_pose[0] + 1][current_pose[1] - 1].color == "white":
                    possible_moves.insert(0, (current_pose,
                                              (current_pose[0] + 1,
                                               current_pose[1] - 1), False))
                if current_board[current_pose[0] + 1][current_pose[1] - 1].color == "black":
                    current_board[current_pose[0] + 1][current_pose[1] - 1].status = True
            except Exception:
                pass

            # en passant for black
            if current_pose[0] == 4:
                try:
                    if current_board[4][current_pose[1] + 1].color == "white" and \
                       current_board[4][current_pose[1] + 1].name == "Pawn" and \
                       prevboard[6][current_pose[1] + 1].id == current_board[4][current_pose[1] + 1].id:
                        possible_moves.insert(0, (current_pose,
                                                  (5, current_pose[1] + 1),
                                                  False))
                        self.en_passant = (5, current_pose[1] + 1)
                except Exception:
                    pass

                try:
                    if current_board[4][current_pose[1] - 1].color == "white" and \
                       current_board[4][current_pose[1] - 1].name == "Pawn" and \
                       prevboard[6][current_pose[1] - 1].id == current_board[4][current_pose[1] - 1].id:
                        possible_moves.insert(0, (current_pose,
                                                  (5, current_pose[1] - 1),
                                                  False))
                        self.en_passant = (5, current_pose[1] - 1)
                except Exception:
                    pass
        return possible_moves


class King(Piece):

    def __init__(self, id, color, pose, first_move=True, status=False):
        super().__init__(id, color, pose, first_move, status)
        self.name = "King"
        self.symbol = "K"
        self.points = 900
        if color == "black":
            image = "images/b_king.png"
            castle = "kq"
        else:
            image = "images/w_king.png"
            castle = "KQ"
        self.image = image
        self.castle = castle

    def possible_moves(self, current_pose,
                       current_board, prevboard=[[]],
                       possible_for_enemy=[]):
        possible_moves = []
        for i in range(-1, 2):
            for n in range(-1, 2):
                if self.color == "white":
                    if current_pose[0] + i >= 0 and current_pose[1] + n >= 0:
                        if current_pose[0] + i != current_pose[0] or \
                           current_pose[1] + n != current_pose[1]:

                            try:
                                if possible_for_enemy[current_pose[0] + i][current_pose[1] + n] == "" and \
                                        current_board[current_pose[0] + i][current_pose[1] + n] == "" or \
                                        possible_for_enemy[current_pose[0] + i][current_pose[1] + n] == "x" and \
                                        current_board[current_pose[0] + i - 1][current_pose[1] + n].name == "Pawn":
                                    possible_moves.append((current_pose,
                                                           (current_pose[0] + i,
                                                            current_pose[1] + n),
                                                           False))
                            except Exception:
                                pass

                            try:
                                if current_board[current_pose[0] + i][current_pose[1] + n].color == "black" and \
                                   current_board[current_pose[0] + i][current_pose[1] + n].status is False:
                                    possible_moves.insert(0, (current_pose,
                                                              (current_pose[0] + i,
                                                               current_pose[1] + n),
                                                              False))
                                if current_board[current_pose[0] + i][current_pose[1] + n].color == "white":
                                    current_board[current_pose[0] + i][current_pose[1] + n].status = True
                            except Exception:
                                pass

                            try:
                                if (current_pose, (current_pose[0] + i, current_pose[1] + n), False) in possible_moves:
                                    for a in range(-1, 2):
                                        for b in range(-1, 2):
                                            if current_pose[0] + i + a >= 0 and current_pose[1] + n + b >= 0:

                                                try:
                                                    if current_board[current_pose[0] + i + a][current_pose[1] + n + b].\
                                                        name == "King" and \
                                                       current_board[current_pose[0] + i + a][current_pose[1] + n + b].\
                                                            color == "black":
                                                        possible_moves.remove((current_pose,
                                                                               (current_pose[0] + i,
                                                                                current_pose[1] + n),
                                                                               False))
                                                except Exception:
                                                    pass
                            except Exception:
                                pass
                if self.color == "black":
                    if current_pose[0] + i >= 0 and current_pose[1] + n >= 0:
                        if current_pose[0] + i != current_pose[0] or current_pose[1] + n != current_pose[1]:

                            try:
                                if possible_for_enemy[current_pose[0] + i][current_pose[1] + n] == "" and \
                                        current_board[current_pose[0] + i][current_pose[1] + n] == "" or \
                                        possible_for_enemy[current_pose[0] + i][current_pose[1] + n] == "x" and \
                                        current_board[current_pose[0] + i + 1][current_pose[1] + n].name == "Pawn":
                                    possible_moves.append((current_pose,
                                                           (current_pose[0] + i,
                                                            current_pose[1] + n),
                                                           False))
                            except Exception:
                                pass

                            try:
                                if current_board[current_pose[0] + i][current_pose[1] + n].color == "white" and \
                                   current_board[current_pose[0] + i][current_pose[1] + n].status is False:
                                    possible_moves.insert(0, (current_pose,
                                                              (current_pose[0] + i,
                                                               current_pose[1] + n),
                                                              False))
                                if current_board[current_pose[0] + i][current_pose[1] + n].color == "black":
                                    current_board[current_pose[0] + i][current_pose[1] + n].status = True
                            except Exception:
                                pass

                            try:
                                if (current_pose, (current_pose[0] + i, current_pose[1] + n), False) in possible_moves:
                                    for a in range(-1, 2):
                                        for b in range(-1, 2):
                                            if current_pose[0] + i + a >= 0 and current_pose[1] + n + b >= 0:

                                                try:
                                                    if current_board[current_pose[0] + i + a][current_pose[1] + n + b].\
                                                        name == "King" and \
                                                       current_board[current_pose[0] + i + a][current_pose[1] + n + b].\
                                                            color == "white":
                                                        possible_moves.remove((current_pose,
                                                                               (current_pose[0] + i,
                                                                                current_pose[1] + n),
                                                                               False))
                                                except Exception:
                                                    pass
                            except Exception:
                                pass
        if self.color == "white":
            try:
                if self.first_move is False or type(current_board[7][7]) == str or \
                   current_board[7][7].symbol != "R" or current_board[7][7].first_move is False:
                    self.castle = self.castle[1:]
                # right side castle
                if self.first_move is True and \
                   current_board[7][7] != "" and \
                   possible_for_enemy[7][5] == "" and current_board[7][5] == "" and \
                   possible_for_enemy[7][6] == "" and current_board[7][6] == "" and \
                   possible_for_enemy[7][4] != 'x':
                    if current_board[7][7].symbol == "R" and current_board[7][7].first_move is True:
                        possible_moves.append((current_pose, (7, 6), False))
            except Exception:
                pass

            try:
                if self.first_move is False or type(current_board[7][0]) == str or \
                   current_board[7][0].symbol != "R" or current_board[7][0].first_move is False:
                    self.castle = self.castle[:-1]
                # left side castle
                if self.first_move is True and \
                   possible_for_enemy[7][3] == "" and current_board[7][3] == "" and \
                   possible_for_enemy[7][2] == "" and current_board[7][2] == "" and \
                   current_board[7][1] == "" and \
                   current_board[7][0] != "" and \
                   possible_for_enemy[7][4] != 'x':
                    if current_board[7][0].symbol == "R" and current_board[7][0].first_move is True:
                        possible_moves.append((current_pose, (7, 2), False))
            except Exception:
                pass

        if self.color == "black":
            try:
                if self.first_move is False or type(current_board[0][7]) == str or \
                   current_board[0][7].symbol != "R" or current_board[0][7].first_move is False:
                    self.castle = self.castle[1:]
                # right side castle
                if self.first_move is True and \
                   possible_for_enemy[0][5] == "" and current_board[0][5] == "" and \
                   possible_for_enemy[0][6] == "" and current_board[0][6] == "" and \
                   current_board[0][7] != "" and \
                   possible_for_enemy[0][4] != 'x':
                    if current_board[0][7].symbol == "R" and current_board[0][7].first_move is True:
                        possible_moves.append((current_pose, (0, 6), False))
            except Exception:
                pass

            try:
                if self.first_move is False or type(current_board[0][0]) == str or \
                   current_board[0][0].symbol != "R" or current_board[0][0].first_move is False:
                    self.castle = self.castle[:-1]
                # left side castle
                if self.first_move is True \
                   and possible_for_enemy[0][3] == "" and current_board[0][3] == "" and \
                   possible_for_enemy[0][2] == "" and current_board[0][2] == "" and \
                   current_board[0][1] == "" and \
                   current_board[0][0] != "" and \
                   possible_for_enemy[0][4] != 'x':
                    if current_board[0][0].symbol == "R" and current_board[0][0].first_move is True:
                        possible_moves.append((current_pose, (0, 2), False))
            except Exception:
                pass
        return possible_moves

    def check_status(self, possible_for_enemy=[[]]):
        if possible_for_enemy[self.pose[0]][self.pose[1]] == "x":
            return True
        else:
            return False

    def checkmate_status(self, check_status, possible_for_ally=[[]]):
        if check_status is True and len(possible_for_ally) == 0:
            return True
        else:
            return False

    def stalemate(self, check_status, possible_for_ally=[[]]):
        if check_status is False and len(possible_for_ally) == 0:
            return True
        else:
            return False


class Queen(Piece):

    def __init__(self, id, color, pose, first_move=True, status=False):
        super().__init__(id, color, pose, first_move, status)
        self.name = "Queen"
        self.symbol = "Q"
        self.points = 90
        if color == "black":
            image = "images/b_queen.png"
        else:
            image = "images/w_queen.png"
        self.image = image

    def possible_moves(self, current_pose, current_board,
                       prevboard=[[]], possible_for_enemy=[[]]):

        w_rook_to_queen = Rook(1, "white", (10, 10))
        b_rook_to_queen = Rook(1, "black", (10, 10))
        w_bishop_to_queen = Bishop(1, "white", (10, 10))
        b_bishop_to_queen = Bishop(1, "black", (10, 10))

        if self.color == "white":
            options_1 = w_rook_to_queen.possible_moves(current_pose,
                                                       current_board)
            options_2 = w_bishop_to_queen.possible_moves(current_pose,
                                                         current_board)
            return options_1 + options_2

        if self.color == "black":
            options_1 = b_rook_to_queen.possible_moves(current_pose,
                                                       current_board)
            options_2 = b_bishop_to_queen.possible_moves(current_pose,
                                                         current_board)
            return options_1 + options_2


class Knight(Piece):

    def __init__(self, id, color, pose, first_move=True, status=False):
        super().__init__(id, color, pose, first_move, status)
        self.name = "Knight"
        self.symbol = "N"
        self.points = 30
        if color == "black":
            image = "images/b_knight.png"
        else:
            image = "images/w_knight.png"
        self.image = image

    def possible_moves(self, current_pose, current_board,
                       prevboard=[[]], possible_for_enemy=[[]]):
        possible_moves = []
        for i in range(-2, 5, 4):
            for n in range(-1, 2, 2):
                try:
                    if current_pose[0] + i >= 0 and current_pose[1] + n >= 0:
                        if current_board[current_pose[0] + i][current_pose[1] + n] == "":
                            possible_moves.append((current_pose,
                                                   (current_pose[0] + i,
                                                    current_pose[1] + n),
                                                   False))
                        if current_board[current_pose[0] + i][current_pose[1] + n].color != self.color:
                            possible_moves.insert(0, (current_pose,
                                                      (current_pose[0] + i,
                                                       current_pose[1] + n),
                                                      False))
                        if current_board[current_pose[0] + i][current_pose[1] + n].color == self.color:
                            current_board[current_pose[0] + i][current_pose[1] + n].status = True
                except Exception:
                    pass

                try:
                    if current_pose[0] + n >= 0 and current_pose[1] + i >= 0:
                        if current_board[current_pose[0] + n][current_pose[1] + i] == "":
                            possible_moves.append((current_pose, (current_pose[0] + n, current_pose[1] + i), False))
                        if current_board[current_pose[0] + n][current_pose[1] + i].color != self.color:
                            possible_moves.insert(0, (current_pose, (current_pose[0] + n, current_pose[1] + i), False))
                        if current_board[current_pose[0] + n][current_pose[1] + i].color == self.color:
                            current_board[current_pose[0] + n][current_pose[1] + i].status = True
                except Exception:
                    pass
        return possible_moves

    def move(self, picked_pose):
        self.pose = picked_pose


class Bishop(Piece):

    def __init__(self, id, color, pose, first_move=True, status=False):
        super().__init__(id, color, pose, first_move, status)
        self.name = "Bishop"
        self.symbol = "B"
        self.points = 30
        if color == "black":
            image = "images/b_bishop.png"
        else:
            image = "images/w_bishop.png"
        self.image = image

    def possible_moves(self, current_pose, current_board, prevboard=[[]], possible_for_enemy=[[]]):
        possible_moves = []
        occur_1 = False
        occur_2 = False
        occur_3 = False
        occur_4 = False
        for i in range(1, 8):
            if occur_1 is False:
                try:
                    if current_board[current_pose[0] + i][current_pose[1] + i] == "":
                        possible_moves.append((current_pose, (current_pose[0] + i, current_pose[1] + i), False))
                    elif current_board[current_pose[0] + i][current_pose[1] + i] == "x" or \
                            current_board[current_pose[0] + i][current_pose[1] + i].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0] + i, current_pose[1] + i), False))
                        occur_1 = True
                    elif current_board[current_pose[0] + i][current_pose[1] + i].color == self.color:
                        current_board[current_pose[0] + i][current_pose[1] + i].status = True
                        occur_1 = True
                except Exception:
                    pass

            if occur_2 is False and current_pose[0] - i >= 0 and current_pose[1] - i >= 0:
                try:
                    if current_board[current_pose[0] - i][current_pose[1] - i] == "":
                        possible_moves.append((current_pose, (current_pose[0] - i, current_pose[1] - i), False))
                    elif current_board[current_pose[0] - i][current_pose[1] - i] == "x" or \
                            current_board[current_pose[0] - i][current_pose[1] - i].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0] - i, current_pose[1] - i), False))
                        occur_2 = True
                    elif current_board[current_pose[0] - i][current_pose[1] - i].color == self.color:
                        current_board[current_pose[0] - i][current_pose[1] - i].status = True
                        occur_2 = True
                except Exception:
                    pass

            if occur_3 is False and current_pose[1] - i >= 0:
                try:
                    if current_board[current_pose[0] + i][current_pose[1] - i] == "":
                        possible_moves.append((current_pose, (current_pose[0] + i, current_pose[1] - i), False))
                    elif current_board[current_pose[0] + i][current_pose[1] - i] == "x" or \
                            current_board[current_pose[0] + i][current_pose[1] - i].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0] + i, current_pose[1] - i), False))
                        occur_3 = True
                    elif current_board[current_pose[0] + i][current_pose[1] - i].color == self.color:
                        current_board[current_pose[0] + i][current_pose[1] - i].status = True
                        occur_3 = True
                except Exception:
                    pass

            if occur_4 is False and current_pose[0] - i >= 0:
                try:
                    if current_board[current_pose[0] - i][current_pose[1] + i] == "":
                        possible_moves.append((current_pose, (current_pose[0] - i, current_pose[1] + i), False))
                    elif current_board[current_pose[0] - i][current_pose[1] + i] == "x" or \
                            current_board[current_pose[0] - i][current_pose[1] + i].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0] - i, current_pose[1] + i), False))
                        occur_4 = True
                    elif current_board[current_pose[0] - i][current_pose[1] + i].color == self.color:
                        current_board[current_pose[0] - i][current_pose[1] + i].status = True
                        occur_4 = True
                except Exception:
                    pass
        return possible_moves


class Rook(Piece):

    def __init__(self, id, color, pose, first_move=True, status=False):
        super().__init__(id, color, pose, first_move, status)
        self.name = "Rook"
        self.symbol = "R"
        self.points = 50
        if color == "black":
            image = "images/b_rook.png"
        else:
            image = "images/w_rook.png"
        self.image = image

    def possible_moves(self, current_pose, current_board, prevboard=[[]], possible_for_enemy=[[]]):
        possible_moves = []
        occurance_1 = False
        occurance_2 = False
        occurance_3 = False
        occurance_4 = False
        for i in range(1, 8):
            try:
                if occurance_1 is False:
                    if current_board[current_pose[0] + i][current_pose[1]] == "":
                        possible_moves.append((current_pose, (current_pose[0] + i, current_pose[1]), False))
                    elif current_board[current_pose[0] + i][current_pose[1]] == "x" or \
                            current_board[current_pose[0] + i][current_pose[1]].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0] + i, current_pose[1]), False))
                        occurance_1 = True
                    elif current_board[current_pose[0] + i][current_pose[1]].color == self.color:
                        current_board[current_pose[0] + i][current_pose[1]].status = True
                        occurance_1 = True
            except Exception:
                pass

            try:
                if occurance_2 is False and current_pose[0] - i >= 0:
                    if current_board[current_pose[0] - i][current_pose[1]] == "":
                        possible_moves.append((current_pose, (current_pose[0] - i, current_pose[1]), False))
                    elif current_board[current_pose[0] - i][current_pose[1]] == "x" or \
                            current_board[current_pose[0] - i][current_pose[1]].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0] - i, current_pose[1]), False))
                        occurance_2 = True
                    elif current_board[current_pose[0] - i][current_pose[1]].color == self.color:
                        current_board[current_pose[0] - i][current_pose[1]].status = True
                        occurance_2 = True
            except Exception:
                pass

            try:
                if occurance_3 is False:
                    if current_board[current_pose[0]][current_pose[1] + i] == "":
                        possible_moves.append((current_pose, (current_pose[0], current_pose[1] + i), False))
                    elif current_board[current_pose[0]][current_pose[1] + i] == "x" or \
                            current_board[current_pose[0]][current_pose[1] + i].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0], current_pose[1] + i), False))
                        occurance_3 = True
                    elif current_board[current_pose[0]][current_pose[1] + i].color == self.color:
                        current_board[current_pose[0]][current_pose[1] + i].status = True
                        occurance_3 = True
            except Exception:
                pass

            try:
                if occurance_4 is False and current_pose[1] - i >= 0:
                    if current_board[current_pose[0]][current_pose[1] - i] == "":
                        possible_moves.append((current_pose, (current_pose[0], current_pose[1] - i), False))
                    elif current_board[current_pose[0]][current_pose[1] - i] == "x" or \
                            current_board[current_pose[0]][current_pose[1] - i].color != self.color:
                        possible_moves.insert(0, (current_pose, (current_pose[0], current_pose[1] - i), False))
                        occurance_4 = True
                    elif current_board[current_pose[0]][current_pose[1] - i].color == self.color:
                        current_board[current_pose[0]][current_pose[1] - i].status = True
                        occurance_4 = True
            except Exception:
                pass
        return possible_moves
