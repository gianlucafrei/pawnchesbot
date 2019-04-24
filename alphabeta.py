class AlphaBeta:
    
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def alphabeta_value(self, board, maxmimizing):
        alpha = float('-inf')
        beta = float('inf')
        alphabeta_result = self.alphabeta(board, self.max_depth, alpha, beta, maxmimizing)

        return alphabeta_result

    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        possible_moves = board.possible_moves()

        if depth==0 or len(possible_moves) == 0:
            value = self.static_heuristic(board)
            if value == float('nan'):
                pass

            return value

        if maximizingPlayer:
            value = float('-inf')
            for move in possible_moves:
                next_board = board.move(move)
                value = max(value, self.alphabeta(next_board, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    pass

            return value
        else:
            value = float('+inf')
            for move in possible_moves:
                next_board = board.move(move)
                value = min(value, self.alphabeta(next_board, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    pass

            return value
    
    def static_heuristic(self, board):
        raise("Not implemented exception")
        
        return 0
