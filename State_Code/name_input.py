import pygame
import time

class CharBox:
    @staticmethod
    def createBoxes(num, midbottom, seperation,
                    screen, fontSize, lineWidth, textColour, lineColour):
        """
        num: the number of boxes
        midbottom: the midbottom coord of the whole box group
        seperation: the distance between the middle of each box
        others: see __init__ method
        """
        seperationTotal = seperation * (num-1)
        midbottom1 = (midbottom[0]-seperationTotal//2, midbottom[1])  # the midbottom of the first box
        boxes = []
        for i in range(num):
            # instantiate all the boxes
            x = midbottom1[0] + seperation * i
            y = midbottom[1]
            boxes.append(CharBox(screen, (x, y), fontSize, lineWidth, textColour, lineColour))

        for i, box in enumerate(boxes[:-1]):
            # create the forewards links
            box.next = boxes[i+1]
        for i, box in enumerate(boxes[1:]):
            # create the backwards links
            box.previous = boxes[i]
        
        boxes[0].active = True
        return boxes[0]

                      
    def __init__(self, screen, midbottom, fontSize, lineWidth, textColour, lineColour):
        """
        screen: the surface that should be drawn onto
        midbottom: the coordinate of the middle of the bottom side
        fontSize: size of the font
        lineWidth: width of the underline
        textColour: the text colour
        lineColour: the colour of the underline
        """
        self.screen = screen
        self.midbottom = midbottom
        self.fontSize = fontSize
        self.midbottom = midbottom
        self.next = None
        self.previous = None

        self.char = "A"
        self.textColour = textColour
        self.font = pygame.font.Font(None, int(fontSize-lineWidth))
        self.rect = self.font.render("W",True, (0,0,0)).get_rect(midbottom=self.midbottom)
        self.width = self.font.render("W",True, (0,0,0)).get_width()
        self.underline = pygame.Rect((0,0),(self.width, lineWidth))
        self.underline.midbottom = midbottom
        self.lineColour = lineColour
        
        self.active = False
        self.flashSpeed = 1

    @property
    def flashTime(self):
        return time.time()%self.flashSpeed
        
    def event(self, key):
        if not self.active and self.next:
            self.next.event(key)
            
        elif key == pygame.K_RETURN:
            self.active = False
            if self.next:
                self.next.active = True
        elif key == pygame.K_BACKSPACE:
            self.active = False
            if self.previous:
                self.previous.active = True
        else:
            self.char = chr(key).upper()

    def click(self, mousePos):
        """
        activates any box the mouse is over
        deactivates any others in the chain
        """
        if self.rect.collidepoint(mousePos):
            self.active = True
        else:
            self.active = False
        if self.next:
            self.next.click(mousePos)
        
    def draw(self):
        if self.flashTime>self.flashSpeed/2 and self.active:
            text = self.font.render(self.char, True, self.lineColour)
        else:   
            text = self.font.render(self.char, True, self.textColour)
        textRect = text.get_rect(midbottom=self.midbottom)
        self.screen.blit(text, textRect)
        pygame.draw.rect(self.screen, self.lineColour, self.underline)
        
                
    def drawAll(self):
        """
        draws self and all following boxes
        """
        self.draw()
        if self.next:  # if self.next exists
            self.next.drawAll()

    def returnString(self):
        """
        returns the string of self and all following boxes
        """
        nextString = self.next.returnString() if self.next else ""
        return self.char + nextString
        

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    box = CharBox.createBoxes(3,(250,250),200, screen, 120, 4, (255,255,255), (0,255,0))
    while True:
        screen.fill((0,0,0))
        box.drawAll()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                box.event(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                box.click(pygame.mouse.get_pos())
