import pygame
from pygame.locals import *


class Button:
    """ a class for a basic button object. """
    
    def __init__(self, screen, nextState, nextStateArgs, text,
                 textSize, primaryColour, secondaryColour, centrePos):
        """
        screen: the screen that the button should be drawn to
        nextState: the string key for the state that should be switched to on click
        nextStateArgs: a list of arguments that should be passed to the next state when this button is clicked
        text: a string representing what will be written on the button
        textSize: an integer representing the pixel height of text
        primaryColour: The colour of the text when the mouse isn't over the button
        secondaryColour: The colour of the background when the mouse isn't over the button
            Note: the primary and secondary colours are swapped when the mouse is over the button
        centrePos: a tuple in the form (x,y) representing the centre co-ordinates of the button
        """
        self.screen = screen
        screenWidth, screenHeight = self.screen.get_size()
        
        self.nextState = nextState
        self.nextStateArgs = nextStateArgs
        self.font = pygame.font.Font(None, textSize)
        self.primaryColour = primaryColour
        self.secondaryColour = secondaryColour
        self.defaultText = self.font.render(text, True, self.primaryColour)
        self.secondaryText = self.font.render(text, True, self.secondaryColour)
        self.rect = self.defaultText.get_rect(center=(int(screenWidth / 2) + centrePos[0],
                                                      int(screenHeight / 2) + centrePos[1]))
        self.mouseIsOverMe = True
    
    def draw(self):
        """ draws the button with it's colours dependent on whether the cursor is over it"""
        if not self.mouseIsOverMe:
            pygame.draw.rect(self.screen, self.secondaryColour, self.rect)
            self.screen.blit(self.defaultText, self.rect)
        else:
            pygame.draw.rect(self.screen, self.primaryColour, self.rect)
            self.screen.blit(self.secondaryText, self.rect)

    def update(self, mousepos):
        """ changes the inversion of the button's colours """
        self.mouseIsOverMe = self.isClicked(mousepos)

    def isClicked(self, mousePos):
        """ returns True if the cursor is over the button"""
        return self.rect.collidepoint(mousePos)


class InternalStateButton(Button):
    """
    a class for buttons that change internal state factors
    """
    def __init__(self, screen, returnedArgs, text,
                 textSize, primaryColour, secondaryColour, centrePos):

        self.screen = screen
        screenWidth, screenHeight = self.screen.get_size()
        
        self.returnedArgs = returnedArgs
        self.font = pygame.font.Font(None, textSize)
        self.primaryColour = primaryColour
        self.secondaryColour = secondaryColour
        self.defaultText = self.font.render(text, True, self.primaryColour)
        self.secondaryText = self.font.render(text, True, self.secondaryColour)
        self.rect = self.defaultText.get_rect(center=(int(screenWidth / 2) + centrePos[0],
                                                      int(screenHeight / 2) + centrePos[1]))
        self.mouseIsOverMe = True
