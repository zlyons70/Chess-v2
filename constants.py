'''This module stores the constants used for the board'''
from __future__ import annotations
from typing import Final
__all__ = ("WIDTH", "HEIGHT", "ROWS", "COLS", "SQUARE_SIZE", "DARK", "LIGHT")

WIDTH: Final[int] = 800
HEIGHT: Final[int] = 800
ROWS: Final[int] = 8
COLS: Final[int] = 8
SQUARE_SIZE: Final[int] = WIDTH//COLS

DARK: Final[tuple] = (112, 102, 119)
LIGHT: Final[tuple] = (204, 183, 174)
