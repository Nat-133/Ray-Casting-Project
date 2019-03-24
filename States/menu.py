import sys, os
import pygame

from States import template
from State_Code import button


class Menu(template.State):
    """
    the class resposnible for the main menu
    """
    
    def __init__(self, screen, identifier="menu"):
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
        self.backgroundColour = (75, 75, 75)
        
        self.titleColour = (23,211,221)
        self.titleFont = pygame.font.Font(None,70)
        self.titleText = self.titleFont.render("First Person Game",
                                               True, self.titleColour)
        self.titlePosition = (int(self.screenWidth/2), int(self.screenHeight/2) - 100)

        buttonTextColour = (23,211,221)
        buttonColour = (24, 100, 221)
        
        screenMiddle = (int(self.screenWidth/2), int(self.screenHeight/2))
        self.buttonList = [button.Button(self.screen, "gameplay", {"restart":True, "levelNum": 1}, "Quick Play", 40,
                                         buttonTextColour, buttonColour, (screenMiddle[0], screenMiddle[1])),
                           button.Button(self.screen, "level select", {"restart":True}, "Level Select",
                                         40, buttonTextColour, buttonColour, (screenMiddle[0], screenMiddle[1]+50))]
        self.persistentVar = {}
       
    def startup(self, persistentVar):
        self.nextState = self.id
        self.persistentVar = persistentVar
        self.screen.fill(self.backgroundColour)
        titleRect = self.titleText.get_rect(center=self.titlePosition)
        self.screen.blit(self.titleText, titleRect)
        with open(os.path.relpath("Levels\\last_played_level.txt"), "rb") as f:
            f.seek(0)
            self.buttonList[0].nextStateArgs["levelNum"] = int(f.read())

    def exit(self):
        with open(os.path.relpath("Levels//last_played_level.txt"), "w") as f:
            f.write(str(self.persistentVar["levelNum"]))
        return self.persistentVar

    def draw(self):
        for thing in self.buttonList:
            thing.draw()

    def update(self, dt):
        mousepos = pygame.mouse.get_pos()
        for thing in self.buttonList:
            thing.update(mousepos)

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for thing in self.buttonList:
                if thing.mouseIsOverMe:
                    print(self.persistentVar)
                    print(thing.nextStateArgs)
                    self.persistentVar = {**self.persistentVar, **thing.nextStateArgs}
                    self.nextState = thing.nextState
