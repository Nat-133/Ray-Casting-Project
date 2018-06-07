import os, sys
import pygame
import pickle

import template.template as template

sys.path.append(os.path.relpath(".."))

from Misc import button


class levelSelect(template.State):
    
    def __init__(self, screen, identifier):
        super().__init__(screen, identifier)
        
        self.pages = self.generatePages()
    
    def generatePages(self, screenWidth, screenHeight, rowNum, columnNum,
                      xBorder, yBorder):
        return 1
        
    def getLevels(self):
        """ returns the number of levles in the levels folder """
        files = os.listdir(os.path.relpath("..//Levels"))
        levels = [file for file in files if file[-4:] == ".txt"
                                         and file[:6] == "level_"
                                         and file[6:-4].isdigit()]
        return len(levels)

class Page:
    """
    holds the items to appear on each page and stores the current page
    """
    
    def __init__(self, screen, columnNum, rowNum, xBorder, yBorder):
        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_size()
        
        self.rowNum = rowNum
        self.columnNum = columnNum
        
        self.xBorder = xBorder
        self.yBorder = yBorder
        self.xSpacing = int((self.screenHeight - (self.xBorder * 2))
                            / (self.columnNum - 1))
        self.ySpacing = int((self.screenHeight - (self.yBorder * 2))
                            / (self.rowNum - 1))
    
    @staticmethod
    def getLevels(self):
        """ returns the number of levles in the levels folder """
        files = os.listdir(os.path.relpath("..//Levels"))
        levels = [file for file in files if file[-4:] == ".txt"
                                            and file[:6] == "level_"
                                            and file[6:-4].isdigit()]
        return len(levels)

        

