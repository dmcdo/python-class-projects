import pygame
from pygame.constants import RESIZABLE
from GameView import GameView
from NSelectView import NSelectView

class MainWindow:
    def __init__(self, width, height):
        pygame.display.set_caption('N Queens')
        self._screen = pygame.display.set_mode((width, height), RESIZABLE)

    def exec(self):
        n = 8
        while True:
            n = NSelectView(self._screen, n).exec()
            GameView(self._screen, n).exec()