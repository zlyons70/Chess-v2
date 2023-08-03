'''This file is used to handle game states, turn changes, sending moves to the board'''
from __future__ import annotations
import pygame
from pygame.locals import *
from pygame import surface
from .board import Board

class Game:
    '''Game object'''
    def __init__(self, win: surface) -> None:
        '''Initializes the game object'''
        self._init()
        self.win: surface = win

    def _init(self) -> None:
        '''Initializes the game'''
        self.selected: object = None
        self.board: object = Board()
        self.turn: str = "white"
        self.valid_moves: dict = {}

    def update(self) -> None:
        '''Updates the game'''
        self.board.draw_squares(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self) -> None:
        '''Resets the game'''
        self._init()

    def select(self, pos: int) -> bool:
        '''Selects a piece and returns True if a piece is selected'''
        if self.selected:
            destination: int = self._move(pos)
            if not destination:
                self.selected = None
                self.select(pos)
        piece: object = self.board.get_piece(pos)

        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            if piece.valid_moves == []:
                self.valid_moves = self.board.get_valid_moves(piece)
            else:
                self.valid_moves = piece.valid_moves
                print(piece.valid_moves)
            return True
        return False
    
    def _move(self, pos: int) -> bool:
        '''Moves the piece on the board'''
        piece: object = self.board.get_piece(pos)
        if self.selected and piece == 0 and pos in self.valid_moves:
            self.board.move(self.selected, pos)
            self.change_turn()
        elif self.selected and piece != 0 and piece.color != self.turn and pos in self.valid_moves:
            self.board.capture(self.selected, pos)
            self.change_turn()
        else:
            return False
        return True
        
    def change_turn(self) -> None:
        '''This function changes the turn'''
        self.valid_moves.clear()
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def draw_valid_moves(self, valid_moves: dict) -> None:
        '''This method draws the valid moves for the selected piece'''
        for move in valid_moves:
            pygame.draw.circle(self.win, (15,10,75), (move % 8 * 100 + 50, int(move / 8) * 100 + 50), 20)