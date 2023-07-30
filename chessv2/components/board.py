'''This class is used to create the board object, which handles board state, and drawing'''
from __future__ import annotations
import pygame
from pygame import Surface
from .constants import DARK, LIGHT, SQUARE_SIZE, ROWS

class Board:
    '''Board object stores board state'''
    def __init__(self) -> None:
        self.board:list = [0] * 64
        #self.create_board() 
    
    def draw_squares(self, win: Surface) -> None:
        '''Draws the squares onto the board'''
        win.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_piece(self, pos: int) -> int:
        '''Returns the piece at the given position'''
        return self.board[pos]