'''This file is used to run the game and to handle player mouse inputs'''
from __future__ import annotations
from typing import Final
import pygame
from pygame import Surface
from components.game import Game
from components.constants import WIDTH, HEIGHT, SQUARE_SIZE

FPS: Final[int] = 60
WIN: Final[Surface] = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

def get_pos_from_mouse(pos: tuple[int, int]) -> int:
    '''Returns the array position of user mouse click'''
    x_pos, y_pos = pos
    row = y_pos // SQUARE_SIZE
    col = x_pos // SQUARE_SIZE
    array_pos = row * 8 + col
    return array_pos

def main() -> None:
    '''Handles the main game loop'''
    run: bool = True
    clock: Final[pygame.time.Clock] = pygame.time.Clock()
    game:object = Game(WIN)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected_pos = get_pos_from_mouse(pos)
                game.select(selected_pos)
        game.update()
    pygame.quit()

main()
