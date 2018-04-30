import sys, os
sys.path.append(os.path.relpath(".."))

import template.template as template
from Misc import button

class Menu(template.State):
    
    def __init__(self, screen):
        super().__init__(screen, "menu")
        self.titleColour = (23,211,221)
        self.titleFont = pygame.font.Font(None,100)
        self.titleText = self.titleFone.render("First Person Game",
        									   True,(0,75,0))

        buttonTextColour = (23,211,221)
        buttonColour = (24, 100, 221)
        
