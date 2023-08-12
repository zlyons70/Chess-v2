'''This module stores the logic for the pieces'''
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from typing import Literal
import pygame
from .constants import *

class Piece(metaclass = ABCMeta):
    '''Initializes each piece with a board position and color'''
    # this is how we define slots in python
    __slots__ = ['board_pos', 'color', 'x_pos', 'y_pos', 'valid_moves']
    board_pos: int
    color: str
    x_pos: int
    y_pos: int
    valid_moves: list[int]
    attack_moves: list[int]
    def __init__(self, board_pos: int, color: str) -> None:
        '''Initializes variables each piece will need'''
        self.board_pos: int = board_pos
        self.color: str = color
        self.x_pos: int = 0
        self.y_pos: int = 0
        self.calc_pos()
        self.valid_moves: list[int] = []
        self.attack_moves: list[int] = []

    def calc_pos(self) -> None:
        '''Calculates the x and y position of the piece'''
        self.x_pos = (self.board_pos % 8) * SQUARE_SIZE
        self.y_pos = (self.board_pos // 8) * SQUARE_SIZE

    def move(self, board_pos) -> None:
        '''When a piece is moved this method updates the board position and recalculates x and y'''
        self.board_pos = board_pos
        self.calc_pos()

    def clear_moves(self) -> None:
        '''This method clears the valid moves list'''
        self.valid_moves.clear()

    @abstractmethod
    def get_valid_moves(self, board: object) -> None:
        '''Calculates the valid moves for the piece'''

    @abstractmethod
    def draw(self, win: pygame.Surface) -> None:
        '''Draws the piece on the board'''

    @abstractmethod
    def piece_to_fen(self) -> str:
        '''Converts the piece to a fen character'''

class King(Piece):
    '''Holds the logic for the king'''
    # Slots are used to optimize memory usage by defining the names of the varible
    # dictionarys are created for all objects in python the values in the dictionary
    # are the values of the variables and takes up a lot of memory by creating a dictionary
    # only changes how python would retrieve the data
    __slots__ = ('check', 'queen_side', 'king_side')
    check: bool
    queen_side: bool
    king_side: bool
    '''Check sees if the king is in check'''
    def __init__(self, board_pos: int, color: str) -> None:
        '''King has check, queen side, and king side attributes'''
        super().__init__(board_pos, color)
        self.check: bool = False
        self.queen_side: bool = True
        self.king_side: bool = True

    def get_valid_moves(self, board: object) -> list:
        offset: list = [-9, -8, -7, -1, 1, 7, 8, 9]
        for move in offset:
            if self.board_pos + move >= 0 and self.board_pos + move <= 63 and \
                    abs(self.board_pos % 8 - (self.board_pos + move) % 8) <= 1:
                if board.board[self.board_pos + move] != 0 and board.board[self.board_pos + move].color != self.color:
                    self.valid_moves.append(self.board_pos + move)
                    self.attack_moves.append(self.board_pos + move)
                if board.board[self.board_pos + move] == 0:
                    self.valid_moves.append(self.board_pos + move)
                    self.attack_moves.append(self.board_pos + move)
        return self.valid_moves

    def draw(self, win: pygame.Surface) -> None:
        if self.color == 'white':
            win.blit(WKING, (self.x_pos, self.y_pos))
        else:
            win.blit(BKING, (self.x_pos, self.y_pos))

    # def in_check(self) -> bool:
    #     '''This function checks to see if the king is in check'''
    #     return False

    def piece_to_fen(self) -> str:
        return 'k' if self.color == 'black' else 'K'

class Pawn(Piece):
    '''Holds the logic for the pawn'''
    __slots__ = ('en_passant', 'en_passant_pos', 'attack_moves')
    en_passant: bool
    en_passant_pos: int
    attack_moves: list[int]
    def __init__(self, board_pos: int, color: str) -> None:
        '''Pawn has en passant and en passant position attributes'''
        super().__init__(board_pos, color)
        self.en_passant: bool = False
        self.en_passant_pos: int = None

    def get_valid_moves(self, board: object) -> list:
        '''Calculates the valid moves for the pawn'''
        direction: int = -1 if self.color == 'white' else 1
        if self.y_pos == 100 and self.color == 'black' or (self.y_pos == 600 and self.color == 'white'):
            if board.board[self.board_pos + (16 * direction)] == 0\
                and board.board[self.board_pos + (8 * direction)] == 0:
                self.valid_moves.append(self.board_pos + (16 * direction))
        if board.board[self.board_pos + (8 * direction)] == 0:
            self.valid_moves.append(self.board_pos + (8 * direction))
        if self.board_pos % 8 == 0:
            if self.color == 'white':
                if board.board[self.board_pos - 7] != 0 and board.board[self.board_pos - 7].color != self.color:
                    self.valid_moves.append(self.board_pos - 7)
                    self.attack_moves.append(self.board_pos - 7)
            else:
                if board.board[self.board_pos + 9] != 0 and board.board[self.board_pos + 9].color != self.color:
                    self.valid_moves.append(self.board_pos + 9)
                    self.attack_moves.append(self.board_pos + 9)
        elif self.board_pos % 8 == 7:
            if self.color == 'white':
                if  board.board[self.board_pos - 9] != 0 and board.board[self.board_pos - 9].color != self.color:
                    self.valid_moves.append(self.board_pos - 9)
                    self.attack_moves.append(self.board_pos - 9)
            else:
                if board.board[self.board_pos + 7] != 0 and board.board[self.board_pos + 7].color != self.color:
                    self.valid_moves.append(self.board_pos + 7)
                    self.attack_moves.append(self.board_pos + 7)
        else:
            if board.board[self.board_pos + 7 * direction] != 0 and board.board[self.board_pos + 7 * direction].color != self.color:
                self.valid_moves.append(self.board_pos + 7 * direction)
                self.attack_moves.append(self.board_pos + 7 * direction)
            if board.board[self.board_pos + 9 * direction] != 0 and board.board[self.board_pos + 9 * direction].color != self.color:
                self.valid_moves.append(self.board_pos + 9 * direction)
                self.attack_moves.append(self.board_pos + 9 * direction)
        if board.en_passant != -1:
            print(board.en_passant)
            if self.color == 'white':
                temp = self.board_pos - 9
                if self.board_pos - board.en_passant == -1:
                    self.valid_moves.append(self.board_pos - 7)
                else:
                    if self.board_pos - board.en_passant == 1 and temp % 8 != 7:
                        self.valid_moves.append(self.board_pos - 9)
            else:
                if self.board_pos - board.en_passant == 1:
                    self.valid_moves.append(self.board_pos + 7)
                else:
                    temp = self.board_pos + 9
                    if self.board_pos - board.en_passant == -1 and temp % 8 != 0:
                        self.valid_moves.append(self.board_pos + 9)
        return self.valid_moves

    def draw(self, win: pygame.Surface) -> None:
        if self.color == 'white':
            win.blit(WPAWN, (self.x_pos, self.y_pos))
        else:
            win.blit(BPAWN, (self.x_pos, self.y_pos))

    def piece_to_fen(self) -> str:
        return 'p' if self.color == 'black' else 'P'

class Knight(Piece):
    '''Holds the logic for the knight'''
    __slots__ = ()
    def get_valid_moves(self, board: object) -> list:
        offsets: list = [17, 15, -17, -15, 10, -10, 6, -6]
        col: int = self.board_pos % 8
        for offset in offsets:
            distance: int = (self.board_pos + offset) % 8 - col
            if self.board_pos + offset >= 0 and self.board_pos + offset < 64 and abs(distance) < 3:
                if board.board[self.board_pos + offset] == 0 or board.board[self.board_pos + offset].color != self.color:
                    self.valid_moves.append(self.board_pos + offset)
                    self.attack_moves.append(self.board_pos + offset)
        return self.valid_moves

    def draw(self, win: pygame.Surface) -> None:
        if self.color == 'white':
            win.blit(WKNIGHT, (self.x_pos, self.y_pos))
        else:
            win.blit(BKNIGHT, (self.x_pos, self.y_pos))
    
    def piece_to_fen(self) -> str:
        return 'n' if self.color == 'black' else 'N'

class Bishop(Piece):
    '''Holds the logic for the bishop'''
    __slots__ = ()
    def get_valid_moves(self, board: object) -> list:
        temp: int = self.board_pos + 9
        while temp % 8 <= 7 and temp % 8 > self.board_pos % 8 and temp <= 63:
            if board.board[temp] != 0:
                if board.board[temp] != 0 and board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp += 9
        temp = self.board_pos - 9
        while temp % 8 >= 0 and temp % 8 < self.board_pos % 8 and temp >= 0:
            if board.board[temp] != 0:
                if board.board[temp] != 0 and board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp -= 9
        temp  = self.board_pos - 7
        while temp % 8 <= 7 and temp % 8 > self.board_pos % 8 and temp >= 0:
            if board.board[temp] != 0:
                if board.board[temp] != 0 and board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp -= 7
        temp = self.board_pos + 7
        while temp % 8 >= 0 and temp % 8 < self.board_pos % 8 and temp <= 63:
            if board.board[temp] != 0:
                if board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp += 7
        self.attack_moves.extend(self.valid_moves)
        return self.valid_moves

    def draw(self, win: pygame.Surface) -> None:
        if self.color == 'white':
            win.blit(WBISHOP, (self.x_pos, self.y_pos))
        else:
            win.blit(BBISHOP, (self.x_pos, self.y_pos))

    def piece_to_fen(self) -> str:
        return 'b' if self.color == 'black' else 'B'

class Rook(Piece):
    '''Holds the logic for the rook'''
    __slots__ = ('queen_side', 'king_side', 'moved')
    queen_side: bool
    king_side: bool
    moved: bool
    def __init__(self, board_pos: int, color: str) -> None:
        '''The rook holds properties deteriming if it has moved or not'''
        super().__init__(board_pos, color)
        self.queen_side: bool = True
        self.king_side: bool = True
        self.moved: bool = False
    def get_valid_moves(self, board: object) -> None:
        '''Handels the logic for the rook'''
        temp: int = self.board_pos + 1
        # right move
        while temp % 8 <= 7 and temp % 8 > self.board_pos % 8:
            if board.board[temp] != 0:
                if board.board[temp] != 0 and board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp += 1
        temp = self.board_pos - 1
        # left move
        while temp % 8 >= 0 and temp % 8 < self.board_pos % 8:
            if board.board[temp] != 0:
                if board.board[temp] != 0 and board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp -= 1
        temp = self.board_pos + 8
        # up move
        while temp <= 63:
            if board.board[temp] != 0:
                if board.board[temp] != 0 and board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp += 8
        temp = self.board_pos - 8
        # down move
        while temp >= 0:
            if board.board[temp] != 0:
                if board.board[temp] != 0 and board.board[temp].color == self.color:
                    break
                self.valid_moves.append(temp)
                break
            self.valid_moves.append(temp)
            temp -= 8
        self.moved = True
        self.queen_side = False
        self.king_side = False
        self.attack_moves.extend(self.valid_moves)
        return self.valid_moves

    def draw(self, win: pygame.Surface) -> None:
        if self.color == 'white':
            win.blit(WROOK, (self.x_pos, self.y_pos))
        else:
            win.blit(BROOK, (self.x_pos, self.y_pos))
      
    def piece_to_fen(self) -> str:
        return 'r' if self.color == 'black' else 'R'
        
class Queen(Piece):
    '''Holds the logic for the queen'''
    __slots__ = ()
    def get_valid_moves(self, board: object) -> None:
        '''Uses the rook and bishop logic to generate moves'''
        new_bishop: Bishop = Bishop(self.board_pos, self.color)
        self.valid_moves.extend(new_bishop.get_valid_moves(board))
        del new_bishop
        new_rook: Rook = Rook(self.board_pos, self.color)
        self.valid_moves.extend(new_rook.get_valid_moves(board))
        del new_rook
        self.attack_moves.extend(self.valid_moves)
        return self.valid_moves
    
    def draw(self, win: pygame.Surface) -> None:
        if self.color == 'white':
            win.blit(WQUEEN, (self.x_pos, self.y_pos))
        else:
            win.blit(BQUEEN, (self.x_pos, self.y_pos))
            
    def piece_to_fen(self) -> str:
        return 'q' if self.color == 'black' else 'Q'

# goal: take a square on a board and look at its diagonals, horizontal, and vertical to see if a bishop, rook, etc has vision of the square
# class Checker():
#     '''This class is going to be used to see if a square on the board is in check
#     Used for checkmate and castling'''
#     __slots__ = ('board_obj', 'board_pos', 'color')
#     board_obj: object
#     board_pos: int
#     color: str
#     def __init__(self, board_obj: object, color: str, board_pos: int) -> None:
#         self.board_obj: object = board_obj
#         self.board_pos: int = board_pos
#         self.color: str = color
    
#     def check(self) -> bool:
#         '''Checks if a square is in check'''
#         opp_color: str = 'white' if self.color == 'black' else 'black'
#         new_bishop: Bishop = Bishop(self.board_pos, self.color)
#         new_rook: Rook = Rook(self.board_pos, self.color)
#         new_knight: Knight = Knight(self.board_pos, self.color)
#         for moves in new_bishop.get_valid_moves(self.board_obj):
#             spot_piece: Piece | Literal[0] = self.board_obj.board[moves]
#             if spot_piece != 0 and spot_piece.color != self.color and (isinstance(spot_piece, (Bishop, Queen))):
#                 return True