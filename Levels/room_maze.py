import random


class Cell:
    """
    an individual square in the maze
    """
    def __init__(self, index):
        self.index = index
        self.visited = False
        self.relativeOutLinks = []

    def getUnvisitedNeighbours(self, cells):
        neighbours = []
        i = self.index[0]
        j = self.index[1]
        if not cells[self.index[0] - 1][self.index[1]].visited and i > 0:
            neighbours.append((-1, 0))

        try:
            if not cells[self.index[0] + 1][self.index[1]].visited:
                neighbours.append((1, 0))
        except IndexError:
            pass

        if not cells[self.index[0]][self.index[1] - 1].visited and j > 0:
            neighbours.append((0, -1))

        try:
            if not cells[self.index[0]][self.index[1] + 1].visited:
                neighbours.append((0, 1))
        except IndexError:
            pass

        return neighbours

    def __str__(self):
        return str(self.index)

    def __repr__(self):
        return str(self.index)

    def createOutLink(self, cells):
        self.visited = True
        try:
            relativeOutLink = random.choice(self.getUnvisitedNeighbours(cells))
            
        except IndexError:
            nextCell = None
        else:
            self.relativeOutLinks.append(relativeOutLink)
            nextCell = (self.index[0]+relativeOutLink[0], self.index[1]+relativeOutLink[1])
        return nextCell

class RoomCell(Cell):

    def __init__(self, index, room):
        super().__init__(index)
        self.room = room

    def createDirectOutLink(self, cells):
        """ creates an out link to an adjacent cell """
        return super().createOutLink(cells)
    
    def createOutLink(self, cells):
        """ hands controll over to a room """
        self.visited = True
        return self.room.createOutLink(cells)
    

class Room:
    """
    a group of cells representing a room in the maze
    """
    def __init__(self, topLeft, bottomRight, maze, wallCharacter):
        self.wallCharacter = wallCharacter
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        
        
        #^ the subset of cells that make up the room
        
        
        self.setRoomCells(maze)
        self.cells = [row[topLeft[1]: bottomRight[1]+1]  
                      for row in maze.cells[topLeft[0]: bottomRight[0]+1]]
        self.edgeCells = (self.cells[0] + self.cells[-1] +
                          [row[i] for row in self.cells[1:-1] for i in (0,-1)])
        #^ the cells on the border of the room
        self.setVisitedCells()
    
    def setRoomCells(self, maze):
        """ sets cells in the room to be RoomCell instances """
        for i in range(self.topLeft[0], self.bottomRight[0]+1):
            for j in range(self.topLeft[1], self.bottomRight[1]+1):
                index = (i,j)
                maze.cells[i][j] = RoomCell(index, self)

    def setVisitedCells(self):
        """ makes all interior cells in the room visited """
        for row in self.cells[1:-1]:
            for cell in row[1:-1]:
                cell.visited = True


    def intersects(self, topLeft, bottomRight):
        """ returns true if the rectangle described by the coordinates intersects the room """
        return (topLeft[0] <= self.bottomRight[0] and 
               topLeft[1] <= self.bottomRight[1] and 
               bottomRight[0] >= self.topLeft[0] and 
               bottomRight[1] >= self.topLeft[1])

    def createOutLink(self, cells):
        """ picks a cell to create an outlink from """
        for cell in self.edgeCells:  
            cell.visited = True # marks the room's cells as visited
        try:
            cell = random.choice([c for c in self.edgeCells if c.getUnvisitedNeighbours(cells)])
            #^ chooses a wall cell that has unvisited neighbours
        except IndexError:  # raised if there isn't a cell
            return None
        else:
            return cell.createDirectOutLink(cells)

        
    def __str__(self):
        return str(self.topLeft)

    def __repr__(self):
        return str(self.topLeft)


class Maze:
    wallChars = ["#", "B", "M", "C"]
    
    def __init__(self, width, height):
        self.cells = [[Cell((i, j)) for j in range(width)] for i in range(height)]
        self.rooms = []
        self.width = width
        self.height = height

    def createRooms(self, attempts, maxWidth=5, maxHeight=5):
        """ attempts to create a number of rooms withing the maze"""
        for _ in range(attempts):
            width = random.randint(2, maxWidth)
            height = random.randint(2, maxHeight)
            topLeft = (random.randint(0, self.height-height-1), random.randint(0, self.width-width-1))
            bottomRight = (topLeft[0]+height, topLeft[1]+width)
            wallChar = random.choice(self.wallChars)
            for room in self.rooms:
                if room.intersects(topLeft, bottomRight):
                    break
            else:
                self.rooms.append(Room(topLeft, bottomRight, self, wallChar))

    def createPaths(self):
        unvisitedCells = [cell for row in self.cells for cell in row if not cell.visited]
        while unvisitedCells:
            self._createPath(unvisitedCells[0])
            unvisitedCells = [cell for cell in unvisitedCells if not cell.visited]

    def _createPath(self, cell):
        newIndex = cell.createOutLink(self.cells)
        while newIndex:
            #print(self)
            newCell = self.cells[newIndex[0]][newIndex[1]]
            self._createPath(newCell)
            newIndex = cell.createOutLink(self.cells)

    def __str__(self):
        newi = lambda x: x*2+1
        #^ gets the index of a cell's centre in the new list given its index in the maze
        maze = [["#" for _ in range(newi(self.width))] for __ in range(newi(self.height))]
        #^ fully walled maze as a nested list
        
        for room in self.rooms:  # change room walls
            for i in range(newi(room.topLeft[0])-1, newi(room.bottomRight[0])+2):
                for j in range(newi(room.topLeft[1])-1, newi(room.bottomRight[1])+2):
                    maze[i][j] = room.wallCharacter
                    
        for row in self.cells:  # add paths
            for cell in row:
                maze[newi(cell.index[0])][newi(cell.index[1])] = " "
                for link in cell.relativeOutLinks:
                    maze[newi(cell.index[0])+link[0]][newi(cell.index[1])+link[1]] = " "
        
        for room in self.rooms:  # make rooms
            for i in range(newi(room.topLeft[0]), newi(room.bottomRight[0])+1):
                for j in range(newi(room.topLeft[1]), newi(room.bottomRight[1])+1):
                    maze[i][j] = " "
        maze[-2][-2] = "E"  # adds exit
        
        return str(maze).replace("],", "],\n")



