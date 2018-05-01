import pygame
import template.template as template


class Gameplay(template.State):

    def __init__(self, screen):
        super().__init__(screen, "gameplay")