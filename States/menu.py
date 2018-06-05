import sys, os
import pygame
import pickle
sys.path.append(os.path.relpath(".."))

import template.template as template
from Misc import button

class Menu(template.State):
    """
    the class resposnible for the main menu
    """
    
    def __init__(self, screen, nameInDict):
        super().__init__(screen, nameInDict)
        self.backgroundColour = (75, 75, 75)
        
        self.titleColour = (23,211,221)
        self.titleFont = pygame.font.Font(None,70)
        self.titleText = self.titleFont.render("First Person Game",
                                               True, self.titleColour)
        self.titlePosition = (int(self.screenWidth/2), int(self.screenHeight/2) - 100)

        buttonTextColour = (23,211,221)
        buttonColour = (24, 100, 221)
        self.buttonList = [button.Button(self.screen, "gameplay", [1], "Quick Play", 40,
                                         buttonTextColour, buttonColour, (0,0)),
                           button.Button(self.screen, "level select", None, "Level Select",
                                         40, buttonTextColour, buttonColour, (0,50))]
        self.persistentVar = None # a list of arguments passed to the next state

    def startup(self, persistantVar):
        self.persistantVar = persistantVar
        self.screen.fill(self.backgroundColour)
        titleRect = self.titleText.get_rect(center=(self.titlePosition))
        self.screen.blit(self.titleText, titleRect)
        with open(os.path.relpath("..\\Levels\\last_played_level.txt"),"rb") as f:
            f.seek(0)
            self.buttonList[0].nextStateArgs = [pickle.load(f)]

    def exit(self):
        return self.persistentVar

    def draw(self):
        for thing in self.buttonList:
            thing.draw()

    def update(self):
        mousepos = pygame.mouse.get_pos()
        for thing in self.buttonList:
            thing.update(mousepos)

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            print("click")
            for thing in self.buttonList:
                if thing.mouseIsOverMe:
                    self.persistentVar = thing.nextStateArgs
                    self.nextState = thing.nextState
                
    
    
