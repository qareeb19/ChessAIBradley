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

    def minimaxRoot(self, depth, board, isMaximizing):
        possibleMoves = board.legal_moves
        bestMove = -9999
        secondBest = -9999
        thirdBest = -9999
        bestMoveFinal = None
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            value = max(bestMove, self.minimax(
                depth - 1, board, not isMaximizing))
            board.pop()
            if(value > bestMove):

                thirdBest = secondBest
                secondBest = bestMove
                bestMove = value
                bestMoveFinal = move
        return bestMoveFinal

    def minimax(self, depth, board, is_maximizing):
        if(depth == 0):
            return -self.evaluation(board)
        possibleMoves = board.legal_moves
        if(is_maximizing):
            bestMove = -9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMove = max(bestMove, self.minimax(
                    depth - 1, board, not is_maximizing))
                board.pop()
            return bestMove
        else:
            bestMove = 9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMove = min(bestMove, self.minimax(
                    depth - 1, board, not is_maximizing))
                board.pop()
            return bestMove


# def calculateMove(board):
#    possible_moves = board.legal_moves
#    if(len(possible_moves) == 0):
#        print("No more possible moves...Game Over")
#        sys.exit()
#    bestMove = None
#    bestValue = -9999
#    n = 0
#    for x in possible_moves:
#        move = chess.Move.from_uci(str(x))
#        board.push(move)
#        boardValue = -evaluation(board)
#        board.pop()
#        if(boardValue > bestValue):
#            bestValue = boardValue
#            bestMove = move
#
#    return bestMove


    def evaluation(self, board):
        i = 0
        evaluation = 0
        x = True
        try:
            x = bool(board.piece_at(i).color)
        except AttributeError as e:
            x = x
        while i < 63:
            i += 1
            evaluation = evaluation + \
                (self.getPieceValue(str(board.piece_at(i)))
                 if x else -self.getPieceValue(str(board.piece_at(i))))
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
    #value = value if (board.piece_at(place)).color else -value
        return value

    def move(self, board, time):
        board = chess.Board()
        n = 0

        while n < 100:
            move = self.minimaxRoot(1, board, True)
            move = chess.Move.from_uci(str(move))
            board.push(move)

            n += 1
