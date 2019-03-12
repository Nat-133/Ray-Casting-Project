import pygame

class CharBox:

    def __init__(self, screen, bottomLeft, width, height, lineWidth, textColour, lineColour):
        self.screen = screen
        self.bottomLeft = bottomLeft
        self.width = width
        self.height = height
        self.centre = (bottomLeft[0] + width//2, bottomLeft[1] + height//2)
        
        self.char = "A"
        self.textColour = textColour
        self.font = pygame.font.Font(None, int(0.95*height-lineWidth))        
        self.underline = pygame.Rect(bottomLeft,(width, lineWidth))
        self.lineColour = lineColour

        self.active = False
        

    def update(self, key):
        self.char = chr(key).upper()


    def draw(self):
        text = self.font.render(self.char, True, self.textColour)
        textRect = text.get_rect(center=self.centre)
        self.screen.blit(text, 
