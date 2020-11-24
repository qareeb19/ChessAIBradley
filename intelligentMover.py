import chess
import math
import random
import sys
import numpy


piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 100,
                'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -100}

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


class Player:

    def __init__(self, board, color, time):
        piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 100,
                        'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -100}

    def minimax(self, board, depth, maximize):
        board = chess.Board()
        if board.is_checkmate():
            return -40 if maximize else 40
        elif board.is_game_over():
            return 0

        if depth == 0:
            return self.evaluation(board)

        if maximize:
            bestValue = float("-inf")
            for move in board.legal_moves:
                experimentBoard = board.copy()
                experimentBoard.push(move)
                move, value = self.minimax(experimentBoard, depth, False)
                bestValue = max(bestValue, value)
            return move, bestValue
        else:
            bestValue = float("inf")
            for move in board.legal_moves:
                experimentBoard = board.copy()
                experimentBoard.push(move)
                move, value = self.minimax(experimentBoard, depth - 1, True)
                bestValue = min(bestValue, value)
            return move, bestValue

        return move

    def evaluation(self, board):
        i = 0
        evaluation = 0

        while i < 63:
            i += 1
            if True:
                evaluation = evaluation + \
                    self.getPieceValue(str(board.piece_at(i)))
            else:
                evaluation = 0

            return evaluation

    def getPieceValue(self, piece):
        if(piece == None):
            return 0
        value = 0
        if piece == "P" or piece == "p":
            value = 10
        if piece == "N" or piece == "n":
            value = 30
        if piece == "B" or piece == "b":
            value = 30
        if piece == "R" or piece == "r":
            value = 50
        if piece == "Q" or piece == "q":
            value = 90
        if piece == 'K' or piece == 'k':
            value = 900

        return value

#    def move(self, board, time):
#        return minimax(self, board, 1, 3)

    def move(self, board, time):
        possible_moves = list(board.legal_moves)
        moves = self.minimax(possible_moves, 1, True)
        
        if(len(possible_moves) == 0):
            sys.exit()
        bestMove = None
        bestValue = -9999
        for moves in possible_moves:
            moves = self.minimax(possible_moves, 1, True)
            moves = chess.Move.from_uci(str(moves))
           

            board.push(moves)
            boardValue = -self.evaluation(board) #- self.minimax(board, 1, True)
            board.pop()
            if(boardValue > bestValue):
                bestValue = boardValue
                bestMove = moves
        return bestMove
