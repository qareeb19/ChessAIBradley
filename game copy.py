import chess
import chess.pgn
import time




def positionEvaluation(position, piece_values=piece_values, position_values=position_values):
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
                positionTotalEval += piece_values[piece_type] + flippedPositionArray[rank, file]

            else:
                positionTotalEval += piece_values[piece_type] - positionArray[rank, file]

        return positionTotalEval

def minimax(position, depth, alpha, beta, maximizingPlayer, bestMove = 'h1h3'):
    if depth == 0 or position.is_game_over():
        return positionEvaluation(position, piece_values, position_values), bestMove

    if maximizingPlayer:
        maxEval = -np.inf
        for child in [str(i).replace("Move.from_uci(\'", '').replace('\')', '') for i in list(position.legal_moves)]:
            position.push(chess.Move.from_uci(child))
            eval_position = minimax(position, depth-1, alpha, beta, False)[0]
            position.pop()
            maxEval = np.maximum(maxEval, eval_position)
            alpha = np.maximum(alpha, eval_position)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = np.inf
        minMove = np.inf
        for child in [str(i).replace("Move.from_uci(\'", '').replace('\')', '') for i in list(position.legal_moves)]:
            position.push(chess.Move.from_uci(child))
            eval_position = minimax(position, depth-1, alpha, beta, True)
            position.pop()
            minEval = np.minimum(minEval, eval_position)
            if minEval < minMove:
                minMove = minEval
                bestMin = child

            beta = np.minimum(beta, eval_position)
            if beta <= alpha:
                break

        return minEval, bestMin


