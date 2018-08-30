import os, sys
import json
import time
import pygame
import numpy as np
import template.template as template

sys.path.append(os.path.relpath(".."))

from State_Code import walls
from State_Code import player
from State_Code import raycast

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
        
        self.player = player.Player(1, np.array([1.5, 1.5]), (7*np.pi/4))
        self.fov = np.pi/3
        
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
        rayList =[]
        self.screen.fill((255,255,255))
        angleIncrement = self.fov/self.screenRes[0]
        columnWidth = self.screenWidth/self.screenRes[0]
        angle = (self.player.cameraAngle + (self.fov / 2) + 0.0000001) % (2*np.pi)
        
        beta = int(self.fov/2) + 0.0000001
        x, y = self.player.pos
        bugAngleList = []
        for column in range(int(self.screenRes[0])):
            ray = raycast.Ray(angle, x, y, self.level, self.groundChar)
            rayList.append(ray)
            viewDistance = ray.length
            try:
                #print(np.degrees(angle), np.degrees(angle - self.player.cameraAngle))
                actualDistance = viewDistance * np.cos(angle - self.player.cameraAngle)
                # actualDistance = viewDistance * np.cos(beta)
                topyPos = (self.screenHeight - (1 / actualDistance) * self.screenHeight * 3)/2
                wallHeight = (1 / actualDistance) * self.screenRes[1] * 3
                pygame.draw.rect(self.screen, (actualDistance * 10, actualDistance * 10, actualDistance * 10),
                                 pygame.Rect(column * columnWidth, topyPos, columnWidth, wallHeight))
            except TypeError:
                pass
            angle = (angle - angleIncrement) % (2 * np.pi)
        
        # ############# draws debug mini-map ############# #
        # pygame.draw.rect(self.screen, (200, 200, 200),
        # pygame.Rect(0, 0, self.levelDimensions[0] * 50, self.levelDimensions[1] * 50))
        # for i, row in enumerate(self.level):
        #     for j, block in enumerate(row):
        #         if block == "#":
        #             pygame.draw.rect(self.screen, (0, 0, 0), (
        #             j * 50, i * 50, self.levelDimensions[0] * 50 / len(row),
        #             self.levelDimensions[1] * 50 / len(self.level)))
        #     angle = (angle - angleIncrement) % (2 * np.pi)
        # playerPos = (self.player.pos[0] * 50, self.player.pos[1] * 50)
        # ray1 = rayList[0]
        # ray3 = rayList[int((len(rayList)-1)/2)]
        # ray2 = rayList[-1]
        # pygame.draw.line(self.screen, (255,0,0), playerPos, (ray1.endPos[0]*50, ray1.endPos[1]*50))
        # pygame.draw.line(self.screen, (255, 0, 0), playerPos, (ray2.endPos[0] * 50, ray2.endPos[1] * 50))
        # pygame.draw.line(self.screen, (0, 255, 0), playerPos, (ray3.endPos[0] * 50, ray3.endPos[1] * 50))
        # pygame.display.update()
    
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
    
    # def raycast(self, angle, beta, x, y):
    #     rayList = []
    #     # print(angle)
    #     # ray-casting
    #     verticalHit = False
    #     verticalHitPos = None
    #     verticalHitWall = None
    #     horizontalHit = False
    #     horizontalHitPos = None
    #     horizontalHitWall = None
    #
    #     # ***Vertical intersections*** #
    #     if angle < (np.pi / 2) or angle > ((3 * np.pi) / 2):
    #         dx = 1
    #         x1 = int(x) + dx
    #     else:
    #         dx = -1
    #         x1 = int(x)
    #     dy = 1 / np.tan(-(np.pi / 2) + angle)###
    #
    #     y1 = (x - x1) * np.tan(-angle) + y
    #
    #     currentx, currenty = x1, y1
    #     if dx == 1:  # ray going right
    #         for vertical in range(20):
    #             if not (0 < currentx < (self.levelDimensions[0])):
    #                 break
    #             elif not (0 < currenty < (self.levelDimensions[1])):
    #                 break
    #             square = self.level[int(currenty), currentx]
    #             if square != self.groundChar:
    #                 # print("vertical hit")
    #                 verticalHitPos = (currentx, currenty)
    #                 verticalHitWall = self.wallType[square]
    #                 verticalHit = True
    #                 rayList.append((verticalHitPos[0] * 50, verticalHitPos[1] * 50))
    #                 break
    #             else:
    #                 currentx += dx
    #                 currenty += dy
    #             pygame.draw.line(self.screen, (0,255,255),(self.player.pos[0]*50,self.player.pos[1]*50), (currentx*50,currenty*50))
    #             print("done")
    #             pygame.time.wait(100)
    #             pygame.display.update()
    #     else:  # going left
    #         for vertical in range(20):
    #             if not (0 < currentx < (self.levelDimensions[0])):
    #                 break
    #             elif not (0 < currenty < (self.levelDimensions[1])):
    #                 break
    #             square = self.level[int(currenty), (currentx - 1)]
    #             if square != self.groundChar:
    #                 # print("vertical hit")
    #                 verticalHitPos = (currentx, currenty)
    #                 verticalHitWall = self.wallType[square]
    #                 verticalHit = True
    #                 rayList.append((verticalHitPos[0] * 50, verticalHitPos[1] * 50))
    #                 break
    #             else:
    #                 currentx += dx
    #                 currenty += dy
    #             pygame.draw.line(self.screen, (0, 255, 255), (self.player.pos[0] * 50, self.player.pos[1] * 50),
    #                              (currentx * 50, currenty * 50))
    #             print("done")
    #             pygame.time.wait(100)
    #             pygame.display.update()
    #
    #     pygame.display.update()
    #     pygame.time.wait(100)
    #     # ***Horizontal Intersections*** #
    #     if angle < np.pi:
    #         dy = -1
    #         y1 = int(y)
    #     else:
    #         dy = 1
    #         y1 = int(y) + dy
    #     dx = (-dy) / np.tan(angle)
    #     x1 = (y - y1) / np.tan(angle) + x
    #     currentx, currenty = x1, y1
    #     if dy == 1:  # ray going down
    #         for horizontal in range(20):
    #             if not (0 < currentx < (self.levelDimensions[0])):
    #                 break
    #             elif not (0 < currenty < (self.levelDimensions[1])):
    #                 break
    #             square = self.level[currenty, int(currentx)]
    #             if square != self.groundChar:
    #                 # print("horizontal hit")
    #                 horizontalHitPos = (currentx, currenty)
    #                 horizontalHitWall = self.wallType[square]
    #                 horizontalHit = True
    #                 rayList.append((horizontalHitPos[0] * 50, horizontalHitPos[1] * 50))
    #                 break
    #             else:
    #                 currentx += dx
    #                 currenty += dy
    #             pygame.draw.line(self.screen, (0, 255, 0), (self.player.pos[0] * 50, self.player.pos[1] * 50),
    #                              (currentx * 50, currenty * 50))
    #             print("done")
    #             pygame.time.wait(100)
    #             pygame.display.update()
    #     else:  # ray going up
    #         for horizontal in range(20):
    #             if not (0 < currentx < (self.levelDimensions[0])):
    #                 break
    #             elif not (0 < currenty < (self.levelDimensions[1])):
    #                 break
    #             square = self.level[currenty - 1, int(currentx)]
    #             if square != self.groundChar:
    #                 # print("horizontal hit")
    #                 horizontalHitPos = (currentx, currenty)
    #                 horizontalHitWall = self.wallType[square]
    #                 horizontalHit = True
    #                 rayList.append((horizontalHitPos[0] * 50, horizontalHitPos[1] * 50))
    #                 break
    #             else:
    #                 currentx += dx
    #                 currenty += dy
    #             pygame.draw.line(self.screen, (0, 255, 0), (self.player.pos[0] * 50, self.player.pos[1] * 50),
    #                              (currentx * 50, currenty * 50))
    #             print("done")
    #             pygame.time.wait(100)
    #             pygame.display.update()
    #
    #     if verticalHit and horizontalHit:
    #         if dx < 0:
    #             if horizontalHitPos[0] < verticalHitPos[0]:
    #                 viewDistance = np.sqrt((x - verticalHitPos[0]) ** 2 + (y - verticalHitPos[1]) ** 2)
    #
    #                 # section = verticalHitWall.getTexture(verticalHitPos[1] % 1)
    #                 # section = pygame.transform.scale(section, ())
    #             else:
    #                 viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
    #         else:
    #             if horizontalHitPos[0] < verticalHitPos[0]:
    #                 viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
    #
    #                 # section = verticalHitWall.getTexture(verticalHitPos[1] % 1)
    #                 # section = pygame.transform.scale(section, ())
    #             else:
    #                 viewDistance = np.sqrt((x - verticalHitPos[0]) ** 2 + (y - verticalHitPos[1]) ** 2)
    #
    #     elif verticalHit:
    #         viewDistance = np.sqrt((x - verticalHitPos[0]) ** 2 + (y - verticalHitPos[1]) ** 2)
    #
    #     elif horizontalHit:
    #         viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
    #     else:
    #         viewDistance = None
    #     return viewDistance, rayList[0]
        
