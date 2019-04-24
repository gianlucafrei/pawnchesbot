class MinMax:

    def __init__(self, max_depth):
        self.max_depth = max_depth

    def minmax_value(self, board, maxmimizing):
        minmax_result = self.minmax(board, self.max_depth, maxmimizing)
        return minmax_result

    def minmax(self, board, depth, maximizingPlayer):

        possible_moves = board.possible_moves()

        if depth==0 or len(possible_moves) == 0:
            val = self.static_heuristic(board)
            if val == float('nan'):
                pass
            return val

        if maximizingPlayer:
            val = float("-inf")
            for mv in possible_moves:
                next_board = board.move(mv)
                mv_val = self.minmax(next_board, depth-1, False)
                val = max(val, mv_val)
            return val
        else:
            val = float('inf')
            for mv in possible_moves:
                next_board = board.move(mv)
                mv_val = self.minmax(next_board, depth-1, True)
                val = min(val, mv_val)
            return val

    def static_heuristic(self, board):
        raise("Not implemented exception")
        return 0
