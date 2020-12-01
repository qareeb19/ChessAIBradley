import chess
import math
import random
import sys
import numpy as np


piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
                'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900}

position_values = {
    #principles to implement -
    #some pieces, specifically kings and pawns are scored differently in the opening, middle and endgame
    #having both bishops gives a bonus, castling gives a permanent advantage for as long as you hold that, isolated pawns recieve a penalty, having 8 pawns is a penalty, 
    # #having double pawns is a penalty, having lonely pawns is a penalty
    'P': np.array([[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                   [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                   [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                   [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                   [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                   [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
                   [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
                   [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]),

    'N': np.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                   [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                   [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                   [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                   [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                   [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                   [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                   [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]),

    'B': np.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                   [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                   [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                   [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                   [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                   [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                   [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                   [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]),

    'R': np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0],
                   [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,  0.0]]),

    'Q': np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                   [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                   [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                   [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                   [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                   [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                   [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
                   [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]),

    'K': np.array([[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                   [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                   [2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
                   [2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]])}


class Player:

    def __init__(self, board, color, time):
        pass

    def positionEvaluation(self, position, piece_values=piece_values, position_values=position_values):
        # Position of pieces is not taken into account for their strength
        if position_values == 'None':
            total_eval = 0
            pieces = list(position.piece_map().values())

            for piece in pieces:
                total_eval += piece_values[str(piece)]
                

            return total_eval

        else:
            positionTotalEval = 0
            pieces = position.piece_map()

            for j in pieces:
                file = chess.square_file(j)
                rank = chess.square_rank(j)

                piece_type = str(pieces[j])
                positionArray = position_values[piece_type.upper()]

                if piece_type.isupper():
                    flippedPositionArray = np.flip(positionArray, axis=0)
                    positionTotalEval += piece_values[piece_type] + \
                        flippedPositionArray[rank, file]

                else:
                    positionTotalEval += piece_values[piece_type] - \
                        positionArray[rank, file] 

            return positionTotalEval
    '''def evaluation(self, board, piece_values = piece_values ):
        i = 0
        evaluation = 0

        while i < 63:
            i += 1
            if True:
                evaluation = evaluation + piece_values[i]
            else:
                evaluation = 0

        return evaluation'''

    def minimax(self, position, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or position.is_game_over():
            return self.positionEvaluation(position)

        if maximizingPlayer:
            maxEval = -np.inf
            for child in list(position.legal_moves):
                position.push(child)
                eval_position = self.minimax(position, depth-1, alpha, beta, False)[0]
                position.pop()
                
                maxEval = np.maximum(maxEval, eval_position)
                alpha = np.maximum(alpha, eval_position)
                if beta <= alpha:
                    break
            return maxEval

        else:
            minEval = np.inf
            minMove = np.inf
            for child in list(position.legal_moves):
                position.push(child)
                eval_position = self.minimax(position, depth-1, alpha, beta, True)
                position.pop()
               
                minEval = np.minimum(minEval, eval_position)
                if minEval < minMove:
                    minMove = minEval
                    bestMin = child

                beta = np.minimum(beta, eval_position)
                if beta <= alpha:
                    break
            str(bestMin).replace('', "Move.from_uci(\'").replace('', '\')')
            return minEval, bestMin
    '''def minimax(self, board, depth, maximize):
        board = chess.Board()
        if board.is_checkmate():
            return -40 if maximize else 40
        elif board.is_game_over():
            return 1

        if depth == 0:
            return self.positionEvaluation(board)

        if maximize:
            bestValue = float("-inf")
            for move in board.legal_moves:
                experimentBoard = board.copy()
                experimentBoard.push(move)
                value = self.minimax(experimentBoard, depth, False)
                bestValue = max(bestValue, value)
            return bestValue
        else:
            bestValue = float("inf")
            for move in board.legal_moves:
                experimentBoard = board.copy()
                experimentBoard.push(move)
                print(move)
                value = self.minimax(experimentBoard, depth - 1, True)

                bestValue = min(bestValue, value)

            return bestValue'''

    def move(self, board, time):
        possible_moves = list(board.legal_moves)
        moves = self.minimax(board, 1, -float("inf"), float("inf"), False)
#        position = self.positionEvaluation(board)
#        print(position)
#        y = int(moves[0])
        if(len(possible_moves) == 0):
            sys.exit()
        bestMove = None
        bestValue = -9999999
        for x in possible_moves:
            board.push(x)
            boardValue = self.positionEvaluation(board) 
            board.pop()
            if(boardValue  > bestValue):
                bestValue = moves[1]
                bestMove = x

        return bestMove
