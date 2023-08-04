'''This class is used to create the board object, which handles board state, and drawing'''
from __future__ import annotations
import pygame
from pygame import Surface
from .constants import DARK, LIGHT, SQUARE_SIZE, ROWS
from .pieces import King, Queen, Pawn, Bishop, Knight, Rook

class Board:
    '''Board object stores board state'''
    def __init__(self) -> None:
        self.board: list = [0] * 64
        self.current_fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.create_board()
        self.board_to_fen()
        self.en_passant: int = -1
        self.pieces: list = []
        self.turn = 'white'
        self.old_piece: object = None
        self.full_move_counter: int = 0
    
    def draw_squares(self, win: Surface) -> None:
        '''Draws the squares onto the board'''
        win.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        self.draw_piece(win)

    def get_piece(self, pos: int) -> object:
        '''Returns the piece at the given position'''
        return self.board[pos]

    def draw_piece(self, win: Surface) -> None:
        '''Draws the pieces onto the board'''
        for piece in self.board:
            if piece != 0:
                piece.draw(win)
    
    def create_board(self) -> None:
        '''This method creates the board'''
        self.fen_to_board(self.current_fen)
        
    def fen_to_board(self, fen: str) -> None:
        '''This method takes a fen string and converts it to a 0-63 array board'''
        space_counter: int = 0
        x_pos: int = 0
        y_pos: int = 0
        
        for char in fen:
            if space_counter > 0:
                return
            if char == ' ':
                space_counter += 1
            elif char == '/':
                y_pos += 100
                x_pos = 0
            elif char.isdigit():
                x_pos += (int(char) * 100)
            else:
                board_position:int = int((y_pos/100 * 8) + x_pos/100)
                if char == 'r':
                    self.board[board_position] = Rook(board_position, 'black')
                elif char == 'n':
                    self.board[board_position] = Knight(board_position, 'black')
                elif char == 'b':
                    self.board[board_position] = Bishop(board_position, 'black')
                elif char == 'q':
                    self.board[board_position] = Queen(board_position, 'black')
                elif char == 'k':
                    self.board[board_position] = King(board_position, 'black')
                elif char == 'p':
                    self.board[board_position] = Pawn(board_position, 'black')
                elif char == 'R':
                    self.board[board_position] = Rook(board_position, 'white')
                elif char == 'N':
                    self.board[board_position] = Knight(board_position, 'white')
                elif char == 'B':
                    self.board[board_position] = Bishop(board_position, 'white')
                elif char == 'Q':
                    self.board[board_position] = Queen(board_position, 'white')
                elif char =='K':
                    self.board[board_position] = King(board_position, 'white')
                elif char == 'P':
                    self.board[board_position] = Pawn(board_position, 'white')
                x_pos += 100
                
    def board_to_fen(self) -> str:
        '''This method takes a 0-63 array board and converts it to a fen string'''
        fen : str = ""
        space_counter: int = 0
        for i, piece in enumerate(self.board):
            if piece != 0:
                if space_counter > 0:
                    fen += str(space_counter)
                space_counter = 0
                fen += piece.piece_to_fen()
            elif piece == 0:
                space_counter += 1
            if i % 8 == 7 and i != 0 and i != 63:
                if space_counter > 0:
                    fen += str(space_counter)
                fen += '/'
                space_counter = 0
            elif i % 8 == 7 and i == 63:
                fen += ' '
        fen += 'w KQkq - 0 1'
        return fen
                
    def get_valid_moves(self, piece: object) -> list:
        '''This method takes a piece object and returns a list of valid moves'''
        valid_moves: list = []
        if piece != 0:
            valid_moves = piece.get_valid_moves(self)
            print("Valid Moves: ", valid_moves)
        return valid_moves
    
    def get_all_pieces(self) -> None:
        '''This method gets all the pieces on the board and places them in a list'''
        for piece in self.board:
            if piece != 0:
                self.pieces.append(piece)
    
    def move(self, piece: object, destination: int) -> None:
        '''This method moves pieces on the board'''
        self.en_passant = -1
        self.board[piece.board_pos] = 0
        self.board[destination] = piece
        previous: int = piece.board_pos
        pawn_direction: int = -1 if piece.color == 'white' else 1
        piece.move(destination)
        # Here I need to check to see if the piece is a pawn for en passant or promotion
        # I also need to check to see if it is a king or rook for castling
        if isinstance(piece, Pawn):
            if piece.y_pos in [0, 700]:
                self.promote(piece)
            if abs(previous - destination) == 16:
                self.en_passant = piece.board_pos
            if previous % 8 != destination % 8 and self.old_piece == 0:
                self.board[destination + (-pawn_direction * 8)] = 0
                print("in the en passant capture method")
                print("En Passant: ", destination + (-pawn_direction * 8))
                
        if isinstance(piece, King):
            piece.king_side = False
            piece.queen_side = False
            
        if isinstance(piece, Rook):
            piece.moved = True
        self.get_all_pieces()
        for piece_on_board in self.pieces:
            piece_on_board.clear_moves()
        self.full_move_counter += 1
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'
        self.old_piece = 0
        
    def capture(self, piece: object, destination: int) -> None:
        '''This method handles capturing pieces'''
        piece_to_capture: object = self.board[destination]
        if piece_to_capture.color != piece.color:
            self.old_piece = piece_to_capture
            self.board[destination] = 0
            del piece_to_capture
            self.move(piece, destination)
    
    def promote(self, piece: object) -> None:
        '''This method handles pawn promotion'''
        self.board[piece.board_pos] = Queen(piece.board_pos, piece.color)
    
    def castle(self, piece: object, destination: int) -> None:
        '''This method handles castling'''
        
    def generate_all_moves(self) -> dict:
        '''This method generates all the moves for all the pieces on the board'''
        legal_moves: dict = {}
        for piece in self.pieces:
            legal_moves[piece.board_pos] = self.get_valid_moves(piece)
        print("Legal Moves: ", legal_moves)
        return legal_moves
