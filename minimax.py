from pieces import Queen
import random


"""
Author: Igor Kraszewski

Some functions for the chess AI which is used in the method of Game class

"""


# calculating possible moves for the AI
def possible_for_AI(board):
    enemy_possible = board.possible_for_enemies(board.turn)
    possible_ally = board.possible_for_allies(enemy_possible, True)
    return possible_ally, enemy_possible


# checking if AI has a promotion situation
def AI_promo(board, current_pose, picked_pose):
    x = current_pose[0]
    y = current_pose[1]
    piece_to_promo = board.board[x][y]
    if piece_to_promo.name == "Pawn" and picked_pose[0] in (0, 7):
        promo_queen = Queen(999, piece_to_promo.color, (x, y))
        return promo_queen
    return None


#  minimax algorithm for chess AI with alpha-beta pruning
def minimax_AI(board, prev_board,
               depth, alpha, beta,
               is_turn_color, eval_colour):
    if depth == 0 or board.gameover or board.draw:
        return None, board.points_diff(eval_colour)
    options, enemy_possible = possible_for_AI(board)
    try:
        best_move = random.choice(options)
    except Exception:
        options, enemy_possible = possible_for_AI(board)
    if is_turn_color:
        max_points = float('-inf')
        for option in options:
            current_pose = (option[0][0], option[0][1])
            picked_pose = (option[1][0], option[1][1])
            promo = AI_promo(board, current_pose, picked_pose)
            board.move(current_pose, picked_pose, promo)
            max_points_update = minimax_AI(board, board.previous_state['board'],
                                           depth - 1, alpha, beta,
                                           False, eval_colour)[1]
            board.undo_move()
            if max_points_update > max_points:
                max_points = max_points_update
                best_move = option
            alpha = max(alpha, max_points_update)
            if beta <= alpha:
                break
        return best_move, max_points
    else:
        min_points = float('inf')
        for option in options:
            current_pose = (option[0][0], option[0][1])
            picked_pose = (option[1][0], option[1][1])
            promo = AI_promo(board, current_pose, picked_pose)
            board.move(current_pose, picked_pose, promo)
            min_points_update = minimax_AI(board, board.previous_state['board'],
                                           depth - 1, alpha, beta,
                                           True, eval_colour)[1]
            board.undo_move()
            if min_points_update < min_points:
                min_points = min_points_update
                best_move = option
            beta = min(beta, min_points_update)
            if beta <= alpha:
                break
        return best_move, min_points
