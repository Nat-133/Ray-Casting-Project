import os, sys
import json
import time
import pygame
import numpy as np
import template.template as template

sys.path.append(os.path.relpath(".."))

from State_Code import walls
from State_Code import player

class Gameplay(template.State):
    groundChar = " "
    wallType = {"#": walls.Wall("test_wall.png")}
    
    def __init__(self, screen, identifier="gameplay"):
        super().__init__(screen, identifier)
        """
        ## attributes in super() ##
        self.nextState
        self.quit
        self.screen
        self.screenWidth, self.screenHeight
        self.persistentVar
        self.id
        """
        self.screenRes = (self.screenWidth/2, self.screenHeight)
        self.levelNum = 1
        self.level = np.array([["#", "#", "#"], ["#", " ", "#"], ["#", "#", "#"]])
        self.levelDimensions = self.level.shape
        self.levelFile = "level_1.txt"
        self.startTime = time.time()
        self.extraTime = 0
        
        self.player = player.Player(1, np.array([1.5, 1.5]), 0)
        self.fov = np.pi/2
        

    def startup(self, persistentVar):
        """
        ### called when the state becomes active
        :param persistentVar: should be a dict with a "levelNum" key
        :return:
        """
        self.nextState = self.id
        self.persistentVar = persistentVar
        if self.persistentVar["restart"]:
            self.extraTime = 0
            self.startTime = time.time()
            self.levelNum = self.persistentVar["levelNum"]
            self.levelFile = f"level_{self.levelNum}.txt"
            with open(os.path.relpath(f"..//Levels//{self.levelFile}"), "r") as f:
                self.level = np.array(json.loads(f.read()))
            self.levelDimensions = self.level.shape
            self.startTime = time.time()
        else:
            self.extraTime = time.time() - self.startTime
            self.startTime = time.time()
            
    def exit(self):
        return self.persistentVar
    
    def draw(self):
        """
        ray casting
        
        :return:
        """
        
        self.screen.fill((255,255,255))
        angleIncrement = self.fov/self.screenRes[0]
        columnWidth = self.screenWidth/self.screenRes[0]
        angle = self.player.cameraAngle + int(self.fov / 2) + 0.0001
        x, y = self.player.pos
        for column in range(int(self.screenRes[0])):
            print(angle)
            # ray-casting
            verticalHit = False
            verticalHitPos = None
            verticalHitWall = None
            horizontalHit = False
            horizontalHitPos = None
            horizontalHitWall = None
            
            # ***Vertical intersections*** #
            if angle < (np.pi/2) or angle < ((3*np.pi) / 4):
                dx = 1
            else:
                dx = -1
            dy = 1/np.tan((np.pi/2) - angle)
            x1 = int(x) + dx
            y1 = (1-(x % 1)) * np.tan(angle) + y
            
            currentx, currenty = x1, y1
            if dx == 1: # ray going right
                for vertical in range(16):
                    if not(0 < currentx < (self.levelDimensions[0])):
                        break
                    elif not(0 < currenty < (self.levelDimensions[1])):
                        break
                    square = self.level[int(currenty), currentx]
                    if square != self.groundChar:
                        verticalHitPos = (currentx, currenty)
                        verticalHitWall = self.wallType[square]
                        verticalHit = True
                        break
                    else:
                        currentx += dx
                        currenty += dy
            else: # going left
                for vertical in range(16):
                    if not(0 < currentx < (self.levelDimensions[0])):
                        break
                    elif not(0 < currenty < (self.levelDimensions[1])):
                        break
                    square = self.level[int(currenty), (currentx-1)]
                    if square != self.groundChar:
                        verticalHitPos = (currentx, currenty)
                        verticalHitWall = self.wallType[square]
                        verticalHit = True
                        break
                    else:
                        currentx += dx
                        currenty += dy
            
            # ***Horizontal Intersections*** #
            if angle < np.pi:
                dy = 1
            else:
                dy = -1
            dx = 1 / np.tan(angle)
            x1 = (1-(y % 1)) * np.tan((np.pi/2) - angle) + x
            y1 = int(y) + dy
            currentx, currenty = x1, y1
            if dy == 1:  # ray going down
                for horizontal in range(16):
                    if not(0 < currentx < (self.levelDimensions[0])):
                        break
                    elif not(0 < currenty < (self.levelDimensions[1])):
                        break
                    square = self.level[currenty,  int(currentx)]
                    if square != self.groundChar:
                        horizontalHitPos = (currentx, currenty)
                        horizontalHitWall = self.wallType[square]
                        horizontalHit = True
                        break
                    else:
                        currentx += dx
                        currenty += dy
            else:  # ray going up
                for horizontal in range(16):
                    if not(0 < currentx < (self.levelDimensions[0])):
                        break
                    elif not(0 < currenty < (self.levelDimensions[1])):
                        break
                    square = self.level[currenty - 1, int(currentx)]
                    if square != self.groundChar:
                        horizontalHitPos = (currentx, currenty)
                        horizontalHitWall = self.wallType[square]
                        horizontalHit = True
                        break
                    else:
                        currentx += dx
                        currenty += dy
            
            if dx < 0:
                if verticalHit and horizontalHit:
                    if horizontalHitPos[0] < verticalHitPos[0]:
                        viewDistance = np.sqrt((x-verticalHitPos[0])**2 + (y-verticalHitPos[1])**2)
                        
                        #section = verticalHitWall.getTexture(verticalHitPos[1] % 1)
                        #section = pygame.transform.scale(section, ())
                    else:
                        viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
                        
                elif verticalHit:
                    viewDistance = np.sqrt((x - verticalHitPos[0]) ** 2 + (y - verticalHitPos[1]) ** 2)
                    
                elif horizontalHit:
                    viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
            try:
                topyPos = int(viewDistance* 30)
                wallHeight = self.screenHeight - topyPos * 2
                pygame.draw.rect(self.screen, (viewDistance * 10, viewDistance * 10, viewDistance * 10),
                                 pygame.Rect(column * columnWidth, topyPos, columnWidth, wallHeight))
            except NameError:
                pass
            angle = (angle - angleIncrement) % (2 * np.pi)
        thing = np.copy(self.level)
        thing[int(self.player.pos[1]),int(self.player.pos[0])] = "P"
        print(thing)
        """
        note to future self: ray casting sort of works, actual fov is somehow ~pi, don't know why
        view of walls being a bit funky may be because of this
        random white space could be caused by this as well, but idk.
        also, you need to create an overhead view that shows the rays.
        """
    
    def update(self, dt):
        """
        changes position and camera angle based on velocities
        also collisions
        :return:
        """
        self.player.move()
        pos = self.player.intPos
        wall = self.level[pos[1], pos[0]]
        if wall != self.groundChar:
            self.wallType[wall].handleCollision(self.player)
        self.player.turn()
        
    def getEvent(self, event):
        """
        movement and camera rotation to change velocity
        pause
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.relVel = np.array([0.1, 0])
            elif event.key == pygame.K_s:
                self.player.relVel = np.array([-0.1, 0])
            elif event.key == pygame.K_a:
                self.player.cameraVel = 0.1
            elif event.key == pygame.K_d:
                self.player.cameraVel = -0.1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.player.relVel = np.array([0, 0])
            elif event.key == pygame.K_s:
                self.player.relVel = np.array([0, 0])
            elif event.key == pygame.K_a:
                self.player.cameraVel = 0
            elif event.key == pygame.K_d:
                self.player.cameraVel = 0
