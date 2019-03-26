import json
import random
import os
import time
import room_maze
class Cell:
    def __init__(self, index):
        self.index = index
        self.visited = False
        self.relativeOutLinks = []
    
    def getUnvisitedNeighbours(self, cells):
        neighbours = []
        i = self.index[0]
        j = self.index[1]
        # up
        if i > 0 and not cells[i - 1][j].visited: # check if cell is in the maze
            neighbours.append((-1, 0))
        # down
        if i < len(cells)-1 and not cells[i + 1][j].visited: 
            neighbours.append((1, 0))
        # left
        if j > 0 and not cells[i][j - 1].visited:
            neighbours.append((0, -1))
        # right
        if j < len(cells[0])-1 and not cells[i][j + 1].visited:
            neighbours.append((0, 1))
        
        return neighbours
    
    def createOutLink(self, cells):
        try:
            relativeOutLink = random.choice(self.getUnvisitedNeighbours(cells))
            self.relativeOutLinks.append(relativeOutLink)
        except IndexError:  # if random.choice is called on an empty list
            relativeOutLink = None
        self.visited = True
        return relativeOutLink
    
    def __repr__(self):
        return str(self.index)


def generateCells(width, height):
    """
    creates a rectangular nested list of Cell instances to represent the maze
    """
    return [[Cell((i, j)) for j in range(width)] for i in range(height)]


def generateMaze(width, height):
    cells = generateCells(height, width)
    cellVisitedStack = [cells[0][0]]
    while len(cellVisitedStack) != 0:  # while there are unvisited cells
        currentCell = cellVisitedStack[-1]  # last element in stack

        if currentCell.index != (height-1, width-1):  # if the cell isn't bottom-right
            relativeIndex = currentCell.createOutLink(cells)
        else:
            relativeIndex = None
            currentCell.visited = True
            
        if relativeIndex is None:  # if the current cell has no unvisited neighbours
            cellVisitedStack.pop()
        else:
            absIndex = (currentCell.index[0] + relativeIndex[0], currentCell.index[1] + relativeIndex[1])
            cellVisitedStack.append(cells[absIndex[0]][absIndex[1]])  # add next cell to stack
    return cells


def newIndex(oldIndex):
    return oldIndex * 2 + 1


def createListMaze(cells):
    maze = [["#" for j in range((len(cells[0])) * 2 + 1)] for i in range((len(cells)) * 2 + 1)]
    # makes a nested list filled with walls
    for row in cells:
        for cell in row:
            maze[newIndex(cell.index[0])][newIndex(cell.index[1])] = " "
            #  removes walls where cells are
            for link in cell.relativeOutLinks:
                maze[newIndex(cell.index[0]) + link[0]][newIndex(cell.index[1]) + link[1]] = " "
                #  removes walls where there are links between cells
    return maze


def getGreatestLevelNum(directoryFiles, check=None):
    check = check if check is not None else len(directoryFiles)
    if f"level_{check}.txt" in directoryFiles:
        return check
    elif check < 1:
        return 0
    else:
        return getGreatestLevelNum(directoryFiles, check-1)


def createMazeFile(w=15, h=15, newLevelNum=None):
    newLevelNum = newLevelNum if newLevelNum else getGreatestLevelNum(os.listdir())+ 1
    # the above allows newLevelNum to be specified by the user
    maze = room_maze.Maze(w, h)
    maze.createRooms((w+h)//2)
    maze.createPaths()
    
    with open(f"level_{newLevelNum}.txt", "w") as f:
        f.write(str(maze).replace("'",'"'))  # saves the maze to a file
    

def generateMultipleMazeFiles(number):
    for _ in range(number):
        createMazeFile()
