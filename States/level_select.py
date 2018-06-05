import os,sys
import pygame
import pickle

import template.template as template
sys.path.append(os.path.relpath(".."))

from Misc import button


class levelSelect(template.State):
    
    def __init__(self):
        super().__init__("levelSelect")
        
        self.rowNum = 4 # Number of button rows 
        self.collumnNum = 4 # Number of button collumns
        self.xBorder = 40
        self.yBorder = 200
        
        self.xSpacing = int((self.screenHeight - (xBorder * 2))
                            / (self.collumnNum - 1))
        self.ySpacing = int((self.screenHeight - (yBorder*2))
                            / (self.rowNum - 1))
        

        
