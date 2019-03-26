import pygame



class Button:
    """ a class for a basic button object. """
    
    def __init__(self, screen, nextState, nextStateArgs, text,
                 textSize, primaryColour, secondaryColour, centrePos, buttonDimensions=(0, 0)):
        """
        screen: the screen that the button should be drawn to
        nextState: the string key for the state that should be switched to on click
        nextStateArgs: a dict of arguments that should be passed to the next state when this button is clicked
        text: a string representing what will be written on the button
        textSize: an integer representing the pixel height of text
        primaryColour: The colour of the text when the mouse isn't over the button
        secondaryColour: The colour of the background when the mouse isn't over the button
            Note: the primary and secondary colours are swapped when the mouse is over the button
        centrePos: a tuple in the form (x,y) representing the centre co-ordinates of the button
        buttonDimensions: a tuple in the form (x,y) representing the width and height of the button
        """
        self.screen = screen
        self.nextState = nextState
        self.nextStateArgs = nextStateArgs
        self.font = pygame.font.Font(None, textSize)
        self.primaryColour = primaryColour
        self.secondaryColour = secondaryColour
        self.text = text
        self.defaultText = self.font.render(text, True, self.primaryColour)
        self.secondaryText = self.font.render(text, True, self.secondaryColour)
        
        if buttonDimensions == (0, 0):
            self.rect = self.defaultText.get_rect(center=centrePos)
            self.textRect = self.defaultText.get_rect(center=centrePos)
        else:
            self.rect = pygame.Rect((0, 0), buttonDimensions)
            self.rect.center = centrePos
            self.textRect = self.defaultText.get_rect(center=(centrePos[0], centrePos[1]))
        self.mouseIsOverMe = False
    
    def draw(self):
        """ draws the button with it's colours dependent on whether the cursor is over it"""
        if not self.mouseIsOverMe:
            pygame.draw.rect(self.screen, self.secondaryColour, self.rect)
            self.screen.blit(self.defaultText, self.textRect)
        else:
            pygame.draw.rect(self.screen, self.primaryColour, self.rect)
            self.screen.blit(self.secondaryText, self.textRect)

    def update(self, mousepos):
        """ changes the inversion of the button's colours """
        self.mouseIsOverMe = self.isClicked(mousepos)

    def isClicked(self, mousePos):
        """ returns True if the cursor is over the button"""
        return self.rect.collidepoint(mousePos)
    
    def __repr__(self):
        return f"Button(position={self.rect.center}, " \
               f"nextState={self.nextState}, arguments={self.nextStateArgs}, text={self.text}"


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
        self.text = text
        self.defaultText = self.font.render(text, True, self.primaryColour)
        self.secondaryText = self.font.render(text, True, self.secondaryColour)
        self.rect = self.defaultText.get_rect(center=(int(centrePos[0]),
                                                      int(centrePos[1])))
        self.textRect = self.rect
        self.mouseIsOverMe = False
    
    def __repr__(self):
        return f"InternalStateButton(position={self.rect.center}, " \
               f"arguments={self.returnedArgs}, text={self.text}"

class MultiButton(Button):
    """
    buttons with a smaller linked button in the topRight
    """
    def __init__(self, screen, primaryNextState, secondaryNextState, nextStateArgs, primaryText,
                 secondaryText, primaryTextSize, textColour, primaryBackgroundColour,
                 secondaryBackgroundColour, centrePos, buttonDimensions):
        self.nextStateArgs = nextStateArgs
        self.primaryButton=Button(screen, primaryNextState, nextStateArgs, primaryText,
                 primaryTextSize, textColour, primaryBackgroundColour, centrePos, buttonDimensions=buttonDimensions)
        self.rect = self.primaryButton.rect
        secondaryButtonSize = buttonDimensions[0]//5
        secondaryFontSize = secondaryButtonSize-2
        secondaryCentre = self.getSecondaryCentrePos(secondaryButtonSize, 2)
        self.secondaryButton = Button(screen, secondaryNextState, nextStateArgs, secondaryText,
                                      secondaryFontSize, textColour, secondaryBackgroundColour,
                                      secondaryCentre, buttonDimensions=(secondaryButtonSize,secondaryButtonSize))
    
    @property
    def nextState(self):
        if self.secondaryButton.mouseIsOverMe:
            return self.secondaryButton.nextState
        else:
            return self.primaryButton.nextState

    @property
    def mouseIsOverMe(self):
        b1 = self.primaryButton.mouseIsOverMe
        b2 = self.secondaryButton.mouseIsOverMe
        return b1 or b2

    def getSecondaryCentrePos(self, buttonSize, offset):
        """
        returns the coordinates of the centre of the secondary button
        """
        topright=(self.rect.topright[0] - offset, self.rect.topright[1] + offset)
        secondaryRect = pygame.Rect(0, 0, buttonSize, buttonSize)
        secondaryRect.topright = topright
        return secondaryRect.center

    def draw(self):
        """ draws the sub buttons"""
        self.primaryButton.draw()
        self.secondaryButton.draw()

    def update(self, mousepos):
        """ updates sub buttons dependent upon each other """
        self.secondaryButton.update(mousepos)
        if self.secondaryButton.mouseIsOverMe:
            #  ensures only one sub button has its colours inverted
            self.primaryButton.mouseIsOverMe = False
        else:
            self.primaryButton.update(mousepos)

    
       
