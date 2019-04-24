import copy
import minmax
import alphabeta

WHITE = 'w'
BLACK = 'b'

ordA = ord('A')

class Move():
    def __init__(self, fromField, toField):
        self.fromField = fromField
        self.toField = toField

    def __str__(self):

        fromR = self.fromField[0] + 1
        fromC = chr(self.fromField[1] + ordA)

        toR = self.toField[0] + 1
        toC = chr(self.toField[1] + ordA)

        return f'{fromR}{fromC}->{toR}{toC}'

class GameBoard():

    def get_possible_moves(self):
        raise Exception("Not implemented")

    def move(self, move, color):
        raise Exception("Not implemented")

    def is_won(self):
        raise Exception("Not implemented")

class Board(GameBoard):

    def __init__(self, size):
        
        self.size = size
        self.next_move = WHITE
        
        # init rows
        self.rows = []
        for i in range(0, size):
            self.rows.append([])
            for _ in range(0, size):
                self.rows[i].append(None)

        # set pawns
        for i in range(0, self.size):
            self.set_field(0, i, WHITE)
            self.set_field(self.size - 1, i, BLACK)

    def _is_valid_field(self, row, column):

        if row < 0 or row >= self.size:
            return False

        if column < 0 or column >= self.size:
            return False

        return True
    
    def set_field(self, row, column, color):

        if not self._is_valid_field(row, column):
            raise Exception(f'Invalid Field r={row} c={column}')

        if color not in (WHITE, BLACK, None):
            raise Exception("Invalid color")
        
        self.rows[row][column] = color

    def get_field(self, row, column):

        if not self._is_valid_field(row, column):
            raise Exception(f'Invalid Field r={row} c={column}')

        return self.rows[row][column]

    def get_all_pieces_position_of_color(self, color):
        
        result = []
        for r in range(self.size):
            for c in range(self.size):
                if self.get_field(r, c) == color:
                    result.append((r, c))

        return result

    def possible_moves(self):

        if self.is_won():
            return []

        white_positions = self.get_all_pieces_position_of_color(WHITE)
        black_positions = self.get_all_pieces_position_of_color(BLACK)

        possible_moves = []

        if self.next_move == WHITE:
            for (r, c) in white_positions:
                # white pieces advance
                if self._is_valid_field(r+1, c):
                    if self.get_field(r+1, c) == None:
                        possible_moves.append(Move((r, c), (r+1, c)))

                # white pieces capture left
                if self._is_valid_field(r+1, c-1):
                    if self.get_field(r+1, c-1) == BLACK:
                        possible_moves.append(Move((r, c), (r+1, c-1)))

                # white pieces capture right
                if self._is_valid_field(r+1, c+1):
                    if self.get_field(r+1, c+1) == BLACK:
                        possible_moves.append(Move((r, c), (r+1, c+1)))
        else:
            for (r, c) in black_positions:
                # black pieces advance
                if self._is_valid_field(r-1, c):
                    if self.get_field(r-1, c) == None:
                        possible_moves.append(Move((r, c), (r-1, c)))

                # black pieces capture left
                if self._is_valid_field(r-1, c-1):
                    if self.get_field(r-1, c-1) == WHITE:
                        possible_moves.append(Move((r, c), (r-1, c-1)))

                # black pieces capture right
                if self._is_valid_field(r-1, c+1):
                    if self.get_field(r-1, c+1) == WHITE:
                        possible_moves.append(Move((r, c), (r-1, c+1)))
        
        return possible_moves

    def _copy(self):

        new_board = Board(self.size)
        new_board.next_move = self.next_move

        new_rows = copy.deepcopy(self.rows)
        new_board.rows = new_rows
        return new_board


    def move(self, move):

        cp = self._copy()

        cp.set_field(move.fromField[0], move.fromField[1], None)
        cp.set_field(move.toField[0], move.toField[1], self.next_move)

        cp.next_move = BLACK if self.next_move == WHITE else WHITE

        return cp

    def is_won(self):
        
        for c in range(self.size):
            
            if self.get_field(self.size-1, c) == WHITE:
                return WHITE
            
            if self.get_field(0, c) == BLACK:
                return BLACK
            
        return False

class Player():

    def __init__(self, color):
        self.color = color

    def select_move(self, board):
        raise("Not implemented exception")

class HumanPlayer(Player):
    def select_move(self, board):
        movesToChoose = board.possible_moves()
        
        self.print_possible_moves(board, movesToChoose)

        while True:
            inp = input("Enter the number of your move: ")
            if inp == 'q':
                exit()
            try:
                nr = int(inp)
                if 1 <= nr <= len(movesToChoose):
                    return movesToChoose[nr-1]
            except:
                print("Please enter a valid move.")
    
    def print_possible_moves(self, board, movesToChoose):
        print("Possible Moves")
        for idx, move in enumerate(movesToChoose):
            print(f'{idx+1}: {move}')


class PwnChessMinMax(minmax.MinMax):

    def static_heuristic(self, board):
        
        if board.is_won() == WHITE:
            return 100
        
        if board.is_won() == BLACK:
            return -100

        # Draw
        if len(board.possible_moves()) == 0:
            return 0
        
        val = 0

        # Number of pieces
        white_positions = board.get_all_pieces_position_of_color(WHITE)
        black_positions = board.get_all_pieces_position_of_color(BLACK)

        val += len(white_positions)
        val -= len(black_positions)

        #point if no pawn on same column
        for pos in white_positions:
            pwns_in_same_col = [bpos for bpos in black_positions if bpos[1] == pos[1]]
            if len(pwns_in_same_col) == 0:
                row = pos[0]
                if row == 0:
                    val += 0.1
                elif row == 1:
                    val += 0.2
                elif row == 2:
                    val += 0.5
                elif row == 3:
                    val += 1.5

        for pos in black_positions:
            pwns_in_same_col = [bpos for bpos in white_positions if bpos[1] == pos[1]]
            if len(pwns_in_same_col) == 0:
                row = pos[0]
                if row == 3:
                    val += 0.1
                elif row == 2:
                    val += 0.2
                elif row == 1:
                    val += 0.5
                elif row == 0:
                    val += 1.5
        
        return val
class PwnChessAlphaBeta(alphabeta.AlphaBeta):

    def static_heuristic(self, board):
        
        if board.is_won() == WHITE:
            return 100
        
        if board.is_won() == BLACK:
            return -100

        # Draw
        if len(board.possible_moves()) == 0:
            return 0
        
        val = 0

        # Number of pieces
        white_positions = board.get_all_pieces_position_of_color(WHITE)
        black_positions = board.get_all_pieces_position_of_color(BLACK)

        val += len(white_positions)
        val -= len(black_positions)

        #point if no pawn on same column
        for pos in white_positions:
            pwns_in_same_col = [bpos for bpos in black_positions if bpos[1] == pos[1]]
            if len(pwns_in_same_col) == 0:
                row = pos[0]
                if row == 0:
                    val += 0.1
                elif row == 1:
                    val += 0.2
                elif row == 2:
                    val += 0.5
                elif row == 3:
                    val += 1.5

        for pos in black_positions:
            pwns_in_same_col = [bpos for bpos in white_positions if bpos[1] == pos[1]]
            if len(pwns_in_same_col) == 0:
                row = pos[0]
                if row == 3:
                    val += 0.1
                elif row == 2:
                    val += 0.2
                elif row == 1:
                    val += 0.5
                elif row == 0:
                    val += 1.5
        
        return val

class AlphaBetaPlayer(Player):

    ab = PwnChessAlphaBeta(5)

    def select_move(self, board):

        possible_moves = board.possible_moves()
        best_move = possible_moves[0]

        if self.color == BLACK:

            best_val = float('inf')

            for mv in possible_moves:
                next_board = board.move(mv)
                mv_val = self.ab.alphabeta_value(next_board, True)
                if mv_val > best_val:
                    best_move = mv
                    best_val = mv_val

        if self.color == WHITE:
            best_val = float('-inf')
            best_move = possible_moves[0]
            
            for mv in possible_moves:
                next_board = board.move(mv)
                mv_val = self.ab.alphabeta_value(next_board, True)
                if mv_val < best_val:
                    best_move = mv
                    best_val = mv_val
        
        print(f"Computer chooses {best_move}")
        return best_move

class ComputerAssistedPlayer(HumanPlayer):

    ab = PwnChessAlphaBeta(4)
    mm = PwnChessMinMax(4)

    def print_possible_moves(self, board, movesToChoose):

        #current_val = self.mm.minmax_value(board, self.color == WHITE)
        current_val = self.ab.alphabeta_value(board, self.color == WHITE)

        print("Possible Moves")
        for idx, move in enumerate(movesToChoose):

            next_board = board.move(move)
            #next_val = self.mm.minmax_value(next_board, self.color == BLACK)
            next_val = self.ab.alphabeta_value(next_board, self.color == BLACK)

            if next_val == float('-inf'):
                diff = "Mate for black"
            elif next_val == float('inf'):
                diff = "Mate for white"
            else:
                diff = next_val - current_val

            print(f'{idx+1}: {move} {diff}')

class MinMaxPlayer(Player):

    mm = PwnChessMinMax(5)

    def select_move(self, board):

        possible_moves = board.possible_moves()
        best_move = possible_moves[0]

        if self.color == BLACK:

            best_val = float('inf')

            for mv in possible_moves:
                next_board = board.move(mv)
                mv_val = self.mm.minmax_value(next_board, True)
                if mv_val > best_val:
                    best_move = mv
                    best_val = mv_val

        if self.color == WHITE:
            best_val = float('-inf')
            best_move = possible_moves[0]
            
            for mv in possible_moves:
                next_board = board.move(mv)
                mv_val = self.mm.minmax_value(next_board, True)
                if mv_val < best_val:
                    best_move = mv
                    best_val = mv_val
        
        print(f"Computer chooses {best_move}")
        return best_move

class BoardPrinter():

    def print_board(self, board):
        size = board.size

        # Print column label
        print('  ', end='')
        for c in range(size):
            lbl = chr(ordA + c)
            print(f'  {lbl} ', end='')
        print('')

        # Print board up to down
        for i in range(size):
            r = size-1-i

            print('   ', end='')
            for c in range(size):
                print('----', end='')
            print('')
            # row label
            print(f'{r+1} ', end='')

            for c in range(size):

                val = board.get_field(r, c)
                print('|', end='')
                if val == WHITE:
                    print(' w ', end='')
                elif val == BLACK:
                    print(' b ', end='')
                else:
                    print('   ', end='')

            print('|')
        
        print('   ', end='')
        for c in range(size):
            print('----', end='')
        print('')

mm = PwnChessMinMax(4)
ab = PwnChessAlphaBeta(4)

class Game():
    
    printer = BoardPrinter()

    def __init__(self, player1, player2, boardSize):
        self.player1 = player1
        self.player2 = player2
        self.board = Board(boardSize)
    
    def start(self):

        self.printer.print_board(self.board)

        val = mm.minmax_value(self.board, True) 
        print(f"Minmax: {val}")
        val = ab.alphabeta_value(self.board, False)
        print(f"AlphaBeta: {val}")

        while True:
            
            print("Select your move white")
            white_move = self.player1.select_move(self.board)
            self.board = self.board.move(white_move)

            self.printer.print_board(self.board)

            val = mm.minmax_value(self.board, False)
            print(f"Minmax: {val}")
            val = ab.alphabeta_value(self.board, False)
            print(f"AlphaBeta: {val}")

            if(self.board.is_won()):
                print("*** WHITE HAS WON ***")
                break

            if len(self.board.possible_moves()) == 0:
                print("*** THIS IS A DRAW ***")
                break

            print("Select your move black")
            white_move = self.player2.select_move(self.board)
            self.board = self.board.move(white_move)
            
            self.printer.print_board(self.board)

            val = mm.minmax_value(self.board, True)
            print(f"Minmax: {val}")
            val = ab.alphabeta_value(self.board, True)
            print(f"AlphaBeta: {val}")

            if(self.board.is_won()):
                print("*** BLACK HAS WON ***")
                break

            if len(self.board.possible_moves()) == 0:
                print("*** THIS IS A DRAW ***")
                break

if __name__ == "__main__":
    
    player1 = ComputerAssistedPlayer(WHITE)
    #player2 = MinMaxPlayer(BLACK)
    player2 = AlphaBetaPlayer(BLACK)
    game = Game(player1, player2, 4)
    game.start()
    
    