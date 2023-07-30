'''This module stores the logic for the pieces'''
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import ClassVar
import pygame
# piece is an abstract class, any function that inherits from piece must implement the functions in piece
class Piece(metaclass = ABCMeta):
    '''Docstring'''
    __slots__ = ("_x", "y", "color")
    
    image: ClassVar[pygame.Surface] = None
    _x: int
    @property
    def x(self) -> int:
        return self._x
    @x.setter
    def set_x(self, x: int) -> None:
        self._x = x
        
    @abstractmethod
    def move(self) -> None:
        pass
    
class King(Piece):
    