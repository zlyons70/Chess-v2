'''This file is used to handle game states, turn changes, sending moves to the board'''
from __future__ import annotations
import pygame
from pygame.locals import *
from pygame import surface
from .board import Board

class Game:
    '''Game object'''
    def __init__(self, win: surface) -> None:
        self._init()
        self.win = win
    
    def _init(self) -> None:
        '''Initializes the game'''
        self.selected = None
        self.board = Board()
        self.turn = "white"
        self.valid_moves = {}
    
    def update(self) -> None:
        '''Updates the game'''
        self.board.draw_squares(self.win)
        pygame.display.update()
    
    def reset(self) -> None:
        '''Resets the game'''
        self._init()

    def select(self, pos: int) -> None:
        '''Selects a piece'''
        if self.selected:
            destination = self._move(pos)
    
    def _move(self, pos: int) -> bool:
        '''checks if a move is valid'''
        return True
        