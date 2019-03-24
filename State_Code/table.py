import itertools
import pygame

class Table:
    """
    displays data on screen as a table
    """
    def __init__(self, screen, topleft, width, rowHeight, textColour,
                 rowColours, data):
        """
        screen: the pygame surface to be drawn onto
        topleft: the topleft coordinate of the table
        width: width of the table
        rowHeight: height of each row
        textColour: colour of all text in the table
        rowColours: the colours of the rows, should be a list of rgb tuples
        data: the data to be stored in the table,
            should be a 2d nexted list with the dimensions of the table
            formatted [[row1data1, row1data2], [row2,data2], ect...]
        """
        self.screen = screen
        self.topleft = topleft
        self.width = width
        self.rowHeight = rowHeight
        self.textColour = textColour
        self.rowColours = rowColours
        self.updateRows(data)

    def updateRows(self, allData):
        """ returns a list of Row objects for all the groups in data """
        colours = itertools.cycle(self.rowColours)
        rows = []
        for data, colour in zip(allData, colours):
            surface = pygame.Surface((self.width, self.rowHeight))
            surface.fill(colour)
            row = Row(surface, self.textColour, data)
            rows.append(row)
        self.rows = rows

    def draw(self):
        """ draws all the rows in the table """
        for i,row in enumerate(self.rows):
            x = self.topleft[0]
            y = self.topleft[1] + (i * self.rowHeight)
            row.draw(self.screen, (x,y))

    
class Row:
    """
    reprisents one row in a table
    """
    def __init__(self, surface, textColour, data):
        """
        surface: the pygame surface that the text will be drawn to
        textColour: the colour of the text
        data: a list of the data to be included in the row
        """
        self.surface = surface
        self.width, self.height = self.surface.get_size()
        self.font = pygame.font.Font(None, self.height)
        self.data = data
        self.collumnNum = len(data)  # the number of collumns
        self.drawData(textColour)

    def drawData(self, textColour):
        """ draws the data to the surface in the right column """
        collumnWidth = self.width//self.collumnNum
        for i, element in enumerate(self.data):
            text = self.font.render(element, True, textColour)
            x = i*collumnWidth+10
            y = self.height//2
            textRect = text.get_rect(midleft=(x,y))
            self.surface.blit(text, textRect)

    def draw(self, surface, pos):
        """draws the row on a specified surface"""
        surface.blit(self.surface, pos)
