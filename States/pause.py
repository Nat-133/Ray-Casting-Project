import os, sys
import pygame

from States import template
from State_Code import button

class Pause(template.State):
    
    def __init__(self, screen, identifier="pause"):
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
        self.textColour = (23, 211, 221)
        self.buttonColour = (24, 100, 221)
        self.background = pygame.Rect(int(self.screenWidth/4), int(self.screenHeight/8),
                                      int(2*self.screenWidth/4), int(2.8*self.screenHeight/4))
        self.titleText = pygame.font.Font(None, int(self.screenHeight/10)).render("Paused", True, self.textColour)
        self.titleRect = self.titleText.get_rect(midtop=(int(self.screenWidth / 2), int(2*self.screenHeight/10)))
        buttonSpacing = 1.5*self.screenHeight/10
        topButtony = int(4*self.screenHeight / 10)
        self.buttonList = [button.Button(self.screen, "menu", {"restart":True}, "Back to Menu",
                                         int(self.screenHeight / 10), self.textColour,
                                         self.buttonColour, (int(self.screenWidth / 2),topButtony)),
                           button.Button(self.screen, "level select", {"restart": True}, "Level Select",
                                         int(self.screenHeight / 10), self.textColour,
                                         self.buttonColour,
                                         (int(self.screenWidth / 2), topButtony+1*buttonSpacing)),
                           button.Button(self.screen, "gameplay", {"restart": False}, "Return",
                                         int(self.screenHeight / 10), self.textColour,
                                         self.buttonColour,
                                         (int(self.screenWidth / 2), topButtony+2*buttonSpacing))]
        self.mouseOveredButton = None
        
    def startup(self, persistentVar):
        self.persistentVar = persistentVar
        self.nextState = self.id
        
    def exit(self):
        return self.persistentVar
    
    def draw(self):
        pygame.draw.rect(self.screen, self.backgroundColour, self.background)
        self.screen.blit(self.titleText, self.titleRect)
        for singleButton in self.buttonList:
            singleButton.draw()
    
    def update(self, dt):
        mousePos = pygame.mouse.get_pos()
        for singleButton in self.buttonList:
            singleButton.update(mousePos)
            if singleButton.mouseIsOverMe:
                self.mouseOveredButton = singleButton
    
    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            try:
                self.nextState = self.mouseOveredButton.nextState
                self.persistentVar.update(self.mouseOveredButton.nextStateArgs)
            except AttributeError:
                pass
