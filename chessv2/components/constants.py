'''This module stores the constants used for the board'''
from __future__ import annotations
from typing import Final
import pygame
__all__ = ("WIDTH", "HEIGHT", "ROWS", "COLS", "SQUARE_SIZE", "DARK", "LIGHT", "BQUEEN", "WQUEEN",
"BKING", 'WKING', "BPAWN", "WPAWN", "BBISHOP", "WBISHOP", "BKNIGHT", "WKNIGHT", "BROOK", "WROOK")

WIDTH: Final[int] = 800
HEIGHT: Final[int] = 800
ROWS: Final[int] = 8
COLS: Final[int] = 8
SQUARE_SIZE: Final[int] = WIDTH//COLS

DARK: Final[tuple] = (112, 102, 119)
LIGHT: Final[tuple] = (204, 183, 174)

BQUEEN: pygame.Surface = pygame.image.load('chessv2/components/images/bQueen.png')
WQUEEN: pygame.Surface = pygame.image.load('chessv2/components/images/wQueen.png')
BKING: pygame.Surface = pygame.image.load('chessv2/components/images/bKing.png')
WKING: pygame.Surface = pygame.image.load('chessv2/components/images/wKing.png')
BPAWN: pygame.Surface = pygame.image.load('chessv2/components/images/bPawn.png')
WPAWN: pygame.Surface = pygame.image.load('chessv2/components/images/wPawn.png')
BBISHOP: pygame.Surface = pygame.image.load('chessv2/components/images/bBishop.png')
WBISHOP: pygame.Surface = pygame.image.load('chessv2/components/images/wBishop.png')
BKNIGHT: pygame.Surface = pygame.image.load('chessv2/components/images/bKnight.png')
WKNIGHT: pygame.Surface = pygame.image.load('chessv2/components/images/wKnight.png')
BROOK: pygame.Surface = pygame.image.load('chessv2/components/images/bRook.png')
WROOK: pygame.Surface = pygame.image.load('chessv2/components/images/wRook.png')
BQUEEN = pygame.transform.scale(BQUEEN, (100,100))
WQUEEN = pygame.transform.scale(WQUEEN, (100,100))
WKING = pygame.transform.scale(WKING, (100,100))
BKING = pygame.transform.scale(BKING, (100,100))
BPAWN = pygame.transform.scale(BPAWN, (100,100))
WPAWN = pygame.transform.scale(WPAWN, (100,100))
BBISHOP = pygame.transform.scale(BBISHOP, (100,100))
WBISHOP = pygame.transform.scale(WBISHOP, (100,100))
BKNIGHT = pygame.transform.scale(BKNIGHT, (100,100))
WKNIGHT = pygame.transform.scale(WKNIGHT, (100,100))
BROOK = pygame.transform.scale(BROOK, (100,100))
WROOK = pygame.transform.scale(WROOK, (100,100))
