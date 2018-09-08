import os
import sys
import pygame
import pickle

import template.template as template

sys.path.append(os.path.relpath(".."))

from Misc import button


class LevelSelect(template.State):
    
    def __init__(self, screen, identifier="level select"):
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
        self.rowNum, self.columnNum = 4, 4
        self.xBorderLeft, self.xBorderRight = 75, 75
        self.yBorderTop, self.yBorderBottom = 125, 100
        
        self.pages = self.generatePages()
        self.currentPage = self.pages[0]
        
        self.backgroundColour = (75, 75, 75)
        self.textColour = (23, 211, 221)
        self.titleText = pygame.font.Font(None, 90).render("Level Select", True, self.textColour)
        self.titleRect = self.titleText.get_rect(center=(int(self.screenWidth/2),40))
        
    def generatePages(self):
        levels = self.getLevels()
        numberOfButtons = len(levels)
        pages = []
        for page in range(int(numberOfButtons/(self.columnNum * self.rowNum))+1):
            pages.append(Page(self.screen, self.columnNum, self.rowNum, self.xBorderLeft, self.xBorderRight,
                              self.yBorderTop, self.yBorderBottom, 85, 80, page, numberOfButtons))
        return pages
        
    @staticmethod
    def getLevels():
        """ returns the number of levles in the levels folder """
        files = os.listdir(os.path.relpath("..//Levels"))
        levels = [file for file in files if file[-4:] == ".txt"
                                         and file[:6] == "level_"
                                         and file[6:-4].isdigit()]
        levels.sort()
        return levels
    
    def startup(self, persistentVar):
        self.persistentVar = persistentVar
        self.pages = self.generatePages()
        self.currentPage = self.pages[0]
        self.nextState = self.id
        self.screen.fill(self.backgroundColour)
        self.screen.blit(self.titleText, self.titleRect)
    
    def exit(self):
        try:
            z = self.persistentVar.copy()
            z.update(self.currentPage.mouseOveredButton.nextStateArgs)
            return z  # above used instead of commented out block because it works in python versions 3.4 or less
            # return {**self.persistentVar,**self.currentPage.mouseOveredButton.nextStateArgs}
        except AttributeError:
            return self.persistentVar
    
    def draw(self):
        self.screen.fill(self.backgroundColour)
        self.currentPage.draw()
        self.screen.blit(self.titleText, self.titleRect)
        
    def update(self, dt):

        self.currentPage.update()
        try:  # this enables wrapping so the next page button on the last page will return to the first page
            oldPage = self.currentPage
            self.currentPage = self.pages[self.currentPage.nextPage]
            oldPage.nextPage = oldPage.pageNum
        except IndexError:
            self.currentPage.nextPage = self.currentPage.pageNum
            self.currentPage = self.pages[0]
        self.nextState = self.currentPage.nextState
        
        self.currentPage.nextState = "level select"
    
    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            try:
                self.currentPage.nextState = self.currentPage.mouseOveredButton.nextState
            except AttributeError:
                try:
                    self.currentPage.nextPage = self.currentPage.mouseOveredButton.returnedArgs[0]
                except AttributeError:
                    pass


class Page:
    """
    holds the items to appear on each page and stores the current page
    """
    
    def __init__(self, screen, columnNum, rowNum, xBorderLeft, xBorderRight, yBorderTop, yBorderBottom,
                 buttonSize, buttonFontSize, pageNumber, maximumButtonIndex):
        self.nextPage = pageNumber
        self.nextState = "level select"
        self.textColour = (23, 211, 221)
        
        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_size()
        
        self.pageNum = pageNumber
        self.rowNum = rowNum
        self.columnNum = columnNum
        self.xBorderLeft, self.xBorderRight = xBorderLeft, xBorderRight
        self.yBorderTop, self.yBorderBottom = yBorderTop, yBorderBottom
#        self.xSpacing = int((self.screenHeight - (self.xBorderTop + self.xBorderBottom))
#                            / (self.columnNum - 1))
#        self.ySpacing = int((self.screenHeight - (self.yBorderTop + self.yBorderBottom))
#                            / (self.rowNum - 1))
        self.buttonSize = (buttonSize, buttonSize)
        self.buttonFontSize = buttonFontSize
        self.buttonList = []
        self.createButtons(maximumButtonIndex)
        self.mouseOveredButton = None
        
        self.pageIndicator = pygame.font.Font(None, 60).render(str(self.pageNum + 1), True, self.textColour)
        self.pageIndicatorRect = self.pageIndicator.get_rect(center=(int(self.screenWidth/2),
                                                             int(self.screenWidth - (self.yBorderBottom / 2)+20)))
        
    def createButtons(self, maximumButtonIndex):
        xButtonSpacing = int((self.screenHeight - (self.xBorderLeft + self.xBorderRight)) / (self.columnNum - 1))
        yButtonSpacing = int((self.screenHeight - (self.yBorderTop + self.yBorderBottom)) / (self.rowNum - 1))
        self.buttonList = []
        buttonsPerPage = self.columnNum * self.rowNum
        firstButtonIndex = (self.pageNum * buttonsPerPage)
        for i in range(buttonsPerPage):
            buttonIndex = firstButtonIndex + i
            if buttonIndex < maximumButtonIndex:
                rowsBeforeButton = int(i / self.columnNum)
                columnsBeforeNum = i % self.rowNum
                buttonCentrePosx = self.xBorderLeft + (xButtonSpacing * columnsBeforeNum)
                buttonCentrePosy = self.yBorderTop + (yButtonSpacing * rowsBeforeButton)
                self.buttonList.append(button.Button(self.screen, "gameplay",
                                                     {"restart":True, "levelNum":buttonIndex + 1},
                                                     f"{buttonIndex + 1}", self.buttonFontSize,
                                                     (23, 211, 221), (24, 100, 221),
                                                     (buttonCentrePosx, buttonCentrePosy), self.buttonSize))
        
        horizontalScreenCentre = int(self.screenWidth/2)
        loweryBorderCentre = int(self.screenWidth - (self.yBorderBottom / 2))
        
        self.buttonList.append(button.InternalStateButton(self.screen, [self.pageNum-1], "<", 40,
                                                          (23, 211, 221), (24, 100, 221),
                                                          (horizontalScreenCentre-80, loweryBorderCentre+20)))
        self.buttonList.append(button.InternalStateButton(self.screen, [self.pageNum + 1], ">", 40,
                                                          (23, 211, 221), (24, 100, 221),
                                                          (horizontalScreenCentre + 80, loweryBorderCentre+20)))
        self.buttonList.append(button.Button(self.screen, "menu", {}, "Back", 40,
                                             (23, 211, 221), (24, 100, 221), (30, 20)))
        
    def draw(self):
        for singleButton in self.buttonList:
            singleButton.draw()
        self.screen.blit(self.pageIndicator, self.pageIndicatorRect)
    
    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.mouseOveredButton = None
        for singleButton in self.buttonList:
            singleButton.update(mousePos)
            if singleButton.mouseIsOverMe:
                self.mouseOveredButton = singleButton
