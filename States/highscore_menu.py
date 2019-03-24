import pygame
import json
import os

from States import template
from State_Code import button
from State_Code import table

class HighscoreMenu(template.State):

    def __init__(self, screen, identifier="highscore menu"):
        super().__init__(screen, identifier)
        self.screenCentre = (self.screenWidth//2, self.screenHeight//2)
        self.backgroundColour = (75, 75, 75)
        self.textColour = (23, 211, 221)
        self.buttonColour = (24, 100, 221)
        self.titleFont = pygame.font.Font(None,60)
        self.title = self.titleFont.render("Level 1 Highscores", True, self.textColour)
        self.titleRect = self.title.get_rect(center=(self.screenCentre[0],30))
        self.buttonList = [button.Button(self.screen, "level select", {"restart":False},
                                         "Back", 40, self.textColour, self.buttonColour,
                                         (30,20))]
        rowHeight = self.screenHeight//15
        self.table = table.Table(self.screen, (0,100), self.screenWidth, rowHeight,
                                 self.textColour, [(125,125,125),(75, 75, 75)],[])
        self.mouseOveredButton = None
        self.levelNum = 1
        

    @property
    def titleText(self):
        return f"Level {self.levelNum} Highscores"
    
    def startup(self, persistentVar):
        self.persistentVar.update(persistentVar)
        self.levelNum = self.persistentVar["levelNum"]
        self.nextState = self.id
        self.screen.fill(self.backgroundColour)

        self.title = self.titleFont.render(self.titleText, True, self.textColour)
        self.titleRect = self.title.get_rect(center=(self.screenCentre[0],50))
        self.screen.blit(self.title, self.titleRect)

        placeholders = [["-","-"] for _ in range(10)]  # placeholders if there arn't 10 scores
        highscores = (self.getHighscores()+placeholders)[:10]
        data = [["Name", "Time"]]+highscores  # includes a title for each collumn
        self.table.updateRows(data)
        self.table.draw()
        
    def exit(self):
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
                    self.persistentVar.update(thing.nextStateArgs)
                    self.nextState = thing.nextState

    def getHighscores(self):
        """
        gets the highscores for the level
        """
        path = os.path.relpath(f"Highscores\\Level_{self.levelNum}.txt")
        try:
            f = open(path, "rb")
        except FileNotFoundError:  # if the file doesn't exist
            highscores=[]
        else:
            highscores = json.loads(f.read())
            f.close()
        roundedHighscores = [(name, str(round(h,3))) for name, h in highscores]
        return roundedHighscores
