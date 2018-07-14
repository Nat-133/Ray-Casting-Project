import pygame
import template.template as template


class Gameplay(template.State):

    def __init__(self, screen, identifier="gameplay"):
        super().__init__(screen, identifier)
        """
        ## attributes in super() ##
        self.nextState
        self.quit
        self.screen
        self.screenWidth, self.screenHeight
        self.persistentVar
        self.id
        """
        self.levelNum = 1
        self.level = []
        self.levelFile = "level_1.txt"
        self.fov = 90

    def startup(self, persistentVar):
        """
        ### called when the state becomes active
        :param persistentVar: should be a a list in the form [level number,  ]
        :return:
        """
        self.persistentVar = persistentVar
        self.levelNum = self.persistentVar[0]
        self.levelFile = f"level_{self.levelNum}.txt"
