from copy import deepcopy

class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.current_player = 'w'

    def display(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def move(self, start, end):
        sx, sy = start
        ex, ey = end
        piece = self.board[sx][sy]
        if (piece.isupper() and self.current_player == 'w') or (piece.islower() and self.current_player == 'b'):
            self.board[ex][ey] = piece
            self.board[sx][sy] = '.'
            self.current_player = 'b' if self.current_player == 'w' else 'w'
            return True
        return False
    
    def get_piece(self, pos):
        x, y = pos
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[x][y]
        return None
    
    def is_valid_pos(self, pos):
        x, y = pos
        return 0 <= x < 8 and 0 <= y < 8

class PieceMoves:
    @staticmethod
    def get_moves(board, pos, current_player):
        piece = board.get_piece(pos)
        if not piece or (piece.isupper() and current_player != 'w') or (piece.islower() and current_player != 'b'):
            return []
        
        piece_type = piece.lower()
        x, y = pos
        
        if piece_type == 'p':
            return PieceMoves._pawn_moves(board, pos, current_player)
        elif piece_type == 'n':
            return PieceMoves._knight_moves(board, pos, current_player)
        elif piece_type == 'b':
            return PieceMoves._bishop_moves(board, pos, current_player)
        elif piece_type == 'r':
            return PieceMoves._rook_moves(board, pos, current_player)
        elif piece_type == 'q':
            return PieceMoves._queen_moves(board, pos, current_player)
        elif piece_type == 'k':
            return PieceMoves._king_moves(board, pos, current_player)
        return []
    
    @staticmethod
    def _pawn_moves(board, pos, current_player):
        moves = []
        x, y = pos
        direction = -1 if current_player == 'w' else 1
        start_row = 6 if current_player == 'w' else 1
        
        new_x = x + direction
        if board.is_valid_pos((new_x, y)) and board.get_piece((new_x, y)) == '.':
            moves.append((new_x, y))
            
            new_x2 = x + 2 * direction
            if x == start_row and board.get_piece((new_x2, y)) == '.':
                moves.append((new_x2, y))
       
        for dy in [-1, 1]:
            new_x = x + direction
            new_y = y + dy
            if board.is_valid_pos((new_x, new_y)):
                target = board.get_piece((new_x, new_y))
                if target and ((current_player == 'w' and target.islower()) or (current_player == 'b' and target.isupper())):
                    moves.append((new_x, new_y))
        
        return moves
    
    @staticmethod
    def _knight_moves(board, pos, current_player):
        moves = []
        x, y = pos
        knight_jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dx, dy in knight_jumps:
            new_x, new_y = x + dx, y + dy
            if board.is_valid_pos((new_x, new_y)):
                target = board.get_piece((new_x, new_y))
                if target == '.' or ((current_player == 'w' and target.islower()) or (current_player == 'b' and target.isupper())):
                    moves.append((new_x, new_y))
        
        return moves
    
    @staticmethod
    def _bishop_moves(board, pos, current_player):
        return PieceMoves._slide_moves(board, pos, current_player, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
    
    @staticmethod
    def _rook_moves(board, pos, current_player):
        return PieceMoves._slide_moves(board, pos, current_player, [(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    @staticmethod
    def _queen_moves(board, pos, current_player):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return PieceMoves._slide_moves(board, pos, current_player, directions)
    
    @staticmethod
    def _slide_moves(board, pos, current_player, directions):
        moves = []
        x, y = pos
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            while board.is_valid_pos((new_x, new_y)):
                target = board.get_piece((new_x, new_y))
                if target == '.':
                    moves.append((new_x, new_y))
                elif ((current_player == 'w' and target.islower()) or (current_player == 'b' and target.isupper())):
                    moves.append((new_x, new_y))
                    break
                else:
                    break
                new_x += dx
                new_y += dy
        
        return moves
    
    @staticmethod
    def _king_moves(board, pos, current_player):
        moves = []
        x, y = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if board.is_valid_pos((new_x, new_y)):
                target = board.get_piece((new_x, new_y))
                if target == '.' or ((current_player == 'w' and target.islower()) or (current_player == 'b' and target.isupper())):
                    moves.append((new_x, new_y))
        
        return moves
    
    @staticmethod
    def is_square_attacked(board, pos, attacker_color):
        for i in range(8):
            for j in range(8):
                piece = board.get_piece((i, j))
                if piece and ((attacker_color == 'w' and piece.isupper()) or (attacker_color == 'b' and piece.islower())):
                    moves = PieceMoves.get_moves(board, (i, j), attacker_color)
                    if pos in moves:
                        return True
        return False

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.move_history = [] 
        self.selected_piece = None
        self.valid_moves = []
    
    def display_with_hints(self, selected_pos=None, threatened_positions=None):
        board_copy = [row[:] for row in self.board.board]
        
        if selected_pos and self.valid_moves:
            sx, sy = selected_pos
            board_copy[sx][sy] = f'[{board_copy[sx][sy]}]'
            
            for move in self.valid_moves:
                mx, my = move
                if board_copy[mx][my] == '.':
                    board_copy[mx][my] = '*'
                else:
                    board_copy[mx][my] = f'×{board_copy[mx][my]}'
        
        if threatened_positions:
            for pos in threatened_positions:
                x, y = pos
                if board_copy[x][y] != '.' and (selected_pos is None or pos != selected_pos):
                    board_copy[x][y] = f'!{board_copy[x][y]}'
        
        print("  a b c d e f g h")
        for i in range(8):
            print(8 - i, end=' ')
            for j in range(8):
                print(board_copy[i][j], end=' ')
            print()
        print()
    
    def get_threatened_pieces(self):
        threatened = []
        opponent = 'b' if self.board.current_player == 'w' else 'w'
        
        king_pos = None
        king_symbol = 'K' if self.board.current_player == 'w' else 'k'
        
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == king_symbol:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece and ((self.board.current_player == 'w' and piece.isupper()) or 
                              (self.board.current_player == 'b' and piece.islower())):
                    if PieceMoves.is_square_attacked(self.board, (i, j), opponent):
                        threatened.append((i, j))
        
        if king_pos and king_pos in threatened:
            print(f"*** ВНИМАНИЕ: Король {'белых' if self.board.current_player == 'w' else 'черных'} под шахом! ***")
        
        return threatened
    
    def get_available_moves_for_piece(self, pos):
        return PieceMoves.get_moves(self.board, pos, self.board.current_player)
    
    def make_move(self, start, end):
        board_state = deepcopy(self.board.board)
        current_player = self.board.current_player
        self.move_history.append((board_state, current_player))
        
        
        success = self.board.move(start, end)
        
        if not success:
            self.move_history.pop()
        
        return success
    
    def undo_move(self, steps=1):
        for _ in range(steps):
            if self.move_history:
                board_state, player = self.move_history.pop()
                self.board.board = deepcopy(board_state)
                self.board.current_player = player
                return True
        return False
    
    def parse_coordinates(self, coord):
        col = ord(coord[0]) - ord('a')
        row = 8 - int(coord[1])
        return (row, col)
    
    def run(self):
        while True:
            threatened = self.get_threatened_pieces()
            self.display_with_hints(threatened_positions=threatened if threatened else None)
            
            move = input("Введите ход (a2 a3), 'hint' и фигуру чтобы посмотреть возможные ходы, 'undo' и фигуру чтобы откатать назад, 'exit' - для выхода: ").strip().split()
            
            if not move:
                continue
                
            if move[0] == 'exit':
                break
            
            elif move[0] == 'undo':
                steps = 1
                if len(move) > 1 and move[1].isdigit():
                    steps = int(move[1])
                if self.undo_move(steps):
                    print(f"Откат на {steps} ход(ов)")
                else:
                    print("Невозможно выполнить откат")
                continue
            
            elif move[0] == 'hint':
                if len(move) < 2:
                    print("Укажите позицию фигуры, например: hint e2")
                    continue
                
                pos = self.parse_coordinates(move[1])
                piece = self.board.get_piece(pos)
                
                if piece and ((self.board.current_player == 'w' and piece.isupper()) or 
                              (self.board.current_player == 'b' and piece.islower())):
                    self.selected_piece = pos
                    self.valid_moves = self.get_available_moves_for_piece(pos)
                    self.display_with_hints(selected_pos=pos, threatened_positions=threatened if threatened else None)
                    print(f"Доступные ходы: {len(self.valid_moves)}")
                else:
                    print("Это не ваша фигура или клетка пуста")
                continue
            
            if len(move) < 2:
                print("Неверный формат ввода")
                continue
            
            try:
                start = self.parse_coordinates(move[0])
                end = self.parse_coordinates(move[1])
                
                if self.selected_piece:
                    if start != self.selected_piece:
                        print("Сначала сбросьте выбор фигуры (используйте hint снова)")
                        continue
                    if end not in self.valid_moves:
                        print("Недопустимый ход для выбранной фигуры")
                        continue
                
                if self.make_move(start, end):
                    self.selected_piece = None
                    self.valid_moves = []
                else:
                    print("Недопустимый ход или не ваша фигура")
                    self.selected_piece = None
                    self.valid_moves = []
                    
            except (IndexError, ValueError):
                print("Ошибка ввода координат. Используйте формат: a2 a3")
                self.selected_piece = None
                self.valid_moves = []




class Board:
    def __init__(self):
        self.grid = [[' ' for _ in range(8)] for _ in range(8)]
        self._init_pieces()
    
    def _init_pieces(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.grid[i][j] = 'b'
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.grid[i][j] = 'w'
    
    def display(self):
        print('  a b c d e f g h')
        for i in range(8):
            print(8 - i, end=' ')
            for j in range(8):
                print(self.grid[i][j], end=' ')
            print(8 - i)
        print('  a b c d e f g h')
    
    def get_piece(self, row, col):
        return self.grid[row][col]
    
    def set_piece(self, row, col, piece):
        self.grid[row][col] = piece
    
    def is_empty(self, row, col):
        return self.grid[row][col] == ' '
    
    def remove_piece(self, row, col):
        self.grid[row][col] = ' '
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.grid[from_row][from_col]
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = ' '
        
        if abs(to_row - from_row) == 2:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            self.grid[mid_row][mid_col] = ' '
        
        if (piece == 'b' and to_row == 7) or (piece == 'w' and to_row == 0):
            self.grid[to_row][to_col] = piece.upper()
        
        return True
    
    def has_pieces(self, player):
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece == player or piece == player.upper():
                    return True
        return False

class MoveValidator:
    @staticmethod
    def coord_to_index(coord):
        col = ord(coord[0]) - ord('a')
        row = 8 - int(coord[1])
        return row, col
    
    @staticmethod
    def is_valid_move(board, from_row, from_col, to_row, to_col, player):
        if to_row < 0 or to_row > 7 or to_col < 0 or to_col > 7:
            return False
        if not board.is_empty(to_row, to_col):
            return False
        
        piece = board.get_piece(from_row, from_col)
        if piece != player and piece != player.upper():
            return False
        
        is_king = piece == player.upper()
        direction = 1 if player == 'b' else -1
        row_diff = to_row - from_row
        col_diff = abs(to_col - from_col)
        
        if not is_king:
            if row_diff != direction or col_diff != 1:
                return False
            return True
        else:
            if abs(row_diff) != abs(col_diff) or abs(row_diff) == 0:
                return False
            return True
    
    @staticmethod
    def is_valid_capture(board, from_row, from_col, to_row, to_col, player):
        if to_row < 0 or to_row > 7 or to_col < 0 or to_col > 7:
            return False
        if not board.is_empty(to_row, to_col):
            return False
        
        piece = board.get_piece(from_row, from_col)
        if piece != player and piece != player.upper():
            return False
        
        is_king = piece == player.upper()
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        if abs(row_diff) != abs(col_diff) or abs(row_diff) != 2:
            return False
        
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        mid_piece = board.get_piece(mid_row, mid_col)
        
        if mid_piece == ' ' or mid_piece == player or mid_piece == player.upper():
            return False
        
        if not is_king:
            if player == 'b' and row_diff != 2:
                return False
            if player == 'w' and row_diff != -2:
                return False
            return True
        else:
            return True
    
    @staticmethod
    def has_captures(board, player):
        for i in range(8):
            for j in range(8):
                piece = board.get_piece(i, j)
                if piece == player or piece == player.upper():
                    for di in [-2, 2]:
                        for dj in [-2, 2]:
                            to_i, to_j = i + di, j + dj
                            if MoveValidator.is_valid_capture(board, i, j, to_i, to_j, player):
                                return True
        return False
    
    @staticmethod
    def get_all_moves(board, player):
        moves = []
        captures = []
        
        for i in range(8):
            for j in range(8):
                piece = board.get_piece(i, j)
                if piece == player or piece == player.upper():
                    for di in [-1, 1]:
                        for dj in [-1, 1]:
                            to_i, to_j = i + di, j + dj
                            if MoveValidator.is_valid_move(board, i, j, to_i, to_j, player):
                                moves.append((i, j, to_i, to_j))
                    
                    for di in [-2, 2]:
                        for dj in [-2, 2]:
                            to_i, to_j = i + di, j + dj
                            if MoveValidator.is_valid_capture(board, i, j, to_i, to_j, player):
                                captures.append((i, j, to_i, to_j))
        
        if captures:
            return captures
        return moves

class Game:
    def __init__(self):
        self.board = Board()
        self.validator = MoveValidator()
        self.current_player = 'b'
    
    def switch_player(self):
        self.current_player = 'w' if self.current_player == 'b' else 'b'
    
    def get_winner(self):
        if not self.board.has_pieces('b'):
            return 'w'
        if not self.board.has_pieces('w'):
            return 'b'
        return None
    
    def process_move(self, from_row, from_col, to_row, to_col):
        is_capture = abs(to_row - from_row) == 2
        
        if is_capture:
            if self.validator.is_valid_capture(self.board, from_row, from_col, to_row, to_col, self.current_player):
                self.board.move_piece(from_row, from_col, to_row, to_col)
                return True, is_capture
        else:
            if self.validator.is_valid_move(self.board, from_row, from_col, to_row, to_col, self.current_player):
                self.board.move_piece(from_row, from_col, to_row, to_col)
                return True, is_capture
        
        return False, is_capture
    
    def play_turn(self):
        self.board.display()
        print(f"Ход {'черных' if self.current_player == 'b' else 'белых'} (b/w)")
        
        if self.validator.has_captures(self.board, self.current_player):
            print("Вы обязаны бить!")
        
        moves = self.validator.get_all_moves(self.board, self.current_player)
        if not moves:
            return False
        
        while True:
            move = input("Введите ход (например: a3 b4): ").strip().split()
            if len(move) != 2:
                print("Неверный формат")
                continue
            
            from_row, from_col = MoveValidator.coord_to_index(move[0])
            to_row, to_col = MoveValidator.coord_to_index(move[1])
            
            valid, is_capture = self.process_move(from_row, from_col, to_row, to_col)
            
            if valid:
                if is_capture and self.validator.has_captures(self.board, self.current_player):
                    piece = self.board.get_piece(to_row, to_col)
                    if (piece == self.current_player or piece == self.current_player.upper()):
                        if self.validator.has_captures(self.board, self.current_player):
                            print("Продолжайте бить!")
                            continue
                break
            else:
                print("Неверный ход")
        
        return True
    
    def run(self):
        while True:
            if not self.play_turn():
                winner = 'w' if self.current_player == 'b' else 'b'
                self.board.display()
                print(f"Игра окончена! Победили {'черные' if winner == 'b' else 'белые'}")
                break
            
            self.switch_player()
            
            winner = self.get_winner()
            if winner:
                self.board.display()
                print(f"Игра окончена! Победили {'черные' if winner == 'b' else 'белые'}")
                break


            
if __name__ == "__main__":
    try:
        vod = int(input('Выберите игру: 1) Шашки 2) Шахматы\nВаш выбор: '))
        if vod == 2:
            game = ChessGame()
            game.run()
        else:
            game = Game()
            game.run()
    except ValueError:
        print("Некорректный ввод! Введите 1 или 2.")
