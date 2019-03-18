import pygame
import os
import json

from States import template
from State_Code import button


class LevelCompleteMenu(template.State):

    def __init__(self, screen, identifier="level complete"):
        super().__init__(screen, identifier)

        self.backgroundColour = (75, 75, 75)
        self.textColour = (23, 211, 221)
        self.buttonColour = (24, 100, 221)
        self.background = pygame.Rect(int(self.screenWidth/8), int(self.screenHeight/8),
                                      int(6*self.screenWidth/8), int(3.2*self.screenHeight/4))
        
        self.levelNum = 1
        self.titleFont = pygame.font.Font(None, int(self.screenHeight/10))
        self.titleText = self.titleFont.render(f"Level {self.levelNum} Complete", True, self.textColour)
        self.titleRect = self.titleText.get_rect(center=(int(self.screenWidth / 2), int(2*self.screenHeight/10)))
        self.highscoreFont = pygame.font.Font(None, int(self.screenHeight/12))
        self.highscoreText = self.highscoreFont.render("", True, self.textColour)
        self.highscoreRect = self.titleText.get_rect(center=(int(self.screenWidth / 2), int(3*self.screenHeight/10)))
        
        ycoord = int(3*self.screenWidth / 4)
        midx = self.screenWidth//2
        buttonSeperation = self.screenWidth//6
        self.buttonList = [button.Button(self.screen, "gameplay", {"levelNum":1,"restart":True}, "Restart",
                                         int(self.screenHeight / 10), self.textColour,
                                         self.buttonColour, (midx-buttonSeperation, ycoord)),
                           button.Button(self.screen, "level select", {"restart": True}, "Level Select",
                                         int(self.screenHeight / 10), self.textColour,
                                         self.buttonColour,(midx, ycoord+self.screenHeight//10)),
                           button.Button(self.screen, "gameplay", {"levelNum":2,"restart": True}, "Next Level",
                                         int(self.screenHeight / 10), self.textColour,
                                         self.buttonColour, (midx+buttonSeperation, ycoord))]

        self.mouseOveredButton = None
        

    def startup(self, persistentVar):
        self.persistentVar.update(persistentVar)
        self.nextState = self.id
        self.levelNum = self.persistentVar["levelNum"]
        self.buttonList[0].nextStateArgs["levelNum"] = self.levelNum
        self.buttonList[-1].nextStateArgs["levelNum"] = self.levelNum+1

        self.titleText = self.titleFont.render(f"Level {self.levelNum} Complete", True, self.textColour)
        self.titleRect = self.titleText.get_rect(center=(int(self.screenWidth / 2), int(2*self.screenHeight/10)))
        
        time = self.persistentVar["time"]
        highscores = self.getHighscores()
        self.newHighscore = any(time<t for n,t in highscores) or highscores == []
        if self.newHighscore:
            topscore = all(time<t for n,t in highscores) or highscores == []
            highscoreMessage = "new highscore" if topscore else "top ten"
            #^ variable highscore message based on position on leaderboard
        else:
            # no new highscore
            highscoreMessage = ""
        self.highscoreText = self.highscoreFont.render(highscoreMessage, True, self.textColour)
        self.highscoreRect = self.titleText.get_rect(center=(int(self.screenWidth / 2), int(3*self.screenHeight/10)))
        
    def exit(self):
        print(self.persistentVar)
        return self.persistentVar
    
    def draw(self):
        pygame.draw.rect(self.screen, self.backgroundColour, self.background)
        self.screen.blit(self.titleText, self.titleRect)
        self.screen.blit(self.highscoreText, self.highscoreRect)
        for singleButton in self.buttonList:
            singleButton.draw()
    
    def update(self, dt):
        mousePos = pygame.mouse.get_pos()
        for singleButton in self.buttonList:
            singleButton.update(mousePos)
            if singleButton.mouseIsOverMe:
                self.mouseOveredButton = singleButton
    
    def getEvent(self, event):
        pass
    
        if event.type == pygame.MOUSEBUTTONUP:
            try:
                mouseIsOverButton = self.mouseOveredButton.mouseIsOverMe
            except AttributeError:  # raised if mouseOveredButton is None
                pass
            else:
                if mouseIsOverButton:
                    # if the button is clicked, update next state and persistentVar
                    self.nextState = self.mouseOveredButton.nextState
                    self.persistentVar.update(self.mouseOveredButton.nextStateArgs)
                else:
                    pass

    def getHighscores(self):
        """
        gets the highscores for the played level
        """
        path = os.path.relpath(f"Highscores\\Level_{self.levelNum}.txt")
        try:
            f = open(path, "rb")
        except FileNotFoundError:  # if the file doesn't exist
            highscores=[]
        else:
            highscores = json.loads(f.read())
            f.close()
        return highscores
            
    
