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
        
        self.player = player.Player(1, np.array([1.5, 1.5]), (np.pi*3/2))
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
        rayList =[]
        self.screen.fill((255,255,255))
        angleIncrement = self.fov/self.screenRes[0]
        columnWidth = self.screenWidth/self.screenRes[0]
        print(self.player.cameraAngle+self.fov/2)
        angle = self.player.cameraAngle + (self.fov / 2) + 0.0001
        
        beta = int(self.fov/2) + 0.0001
        x, y = self.player.pos
        bugAngleList = []
        for column in range(int(self.screenRes[0])):
            bugAngleList.append(angle)
            print(angle)
            viewDistance, ray = self.raycast(angle, beta, x, y)
            rayList.append(ray)
            try:
                actualDistance = viewDistance * np.cos(beta)
                topyPos = int(viewDistance * 30)
                wallHeight = self.screenHeight - topyPos * 2
                pygame.draw.rect(self.screen, (viewDistance * 10, viewDistance * 10, viewDistance * 10),
                                 pygame.Rect(column * columnWidth, topyPos, columnWidth, wallHeight))
                pygame.draw.rect(self.screen,(200,200,200),
                                 pygame.Rect(0,0,self.levelDimensions[0]*50,self.levelDimensions[1]*50))
                
            except TypeError:
                pass
            pygame.draw.rect(self.screen, (200, 200, 200),
                             pygame.Rect(0, 0, self.levelDimensions[0] * 50, self.levelDimensions[1] * 50))
            playerPos = (self.player.pos[0] * 50, self.player.pos[1] * 50)
            for i,pos in enumerate(rayList):
                pygame.draw.line(self.screen, (255-i, 0, 0), playerPos, pos)
            pygame.draw.line(self.screen, (0, 255, 0), playerPos, (
            int(self.player.pos[0] * 50 + self.player.absVel[0] * 50),
            int(self.player.pos[1] * 50 + self.player.absVel[1] * 50)))
            pygame.draw.line(self.screen, (0, 0, 255), playerPos, (
            playerPos[0] + 100 * np.cos(self.player.cameraAngle), playerPos[1] + 100 * np.sin(self.player.cameraAngle)))
            pygame.display.update()
            pygame.time.wait(10)
            beta = (angle - angleIncrement)
            #print("################start####################")
            #for i,angle in enumerate(bugAngleList):
            #    try:
            #        print(angle-bugAngleList[i-1])
            #    except:
            #        pass
            #print("####################END#######################")
            angle = (angle - angleIncrement) % (2 * np.pi)
        thing = np.copy(self.level)
        thing[int(self.player.pos[1]),int(self.player.pos[0])] = "P"
        pygame.draw.rect(self.screen, (200,200,200),pygame.Rect(0,0,self.levelDimensions[0]*50,self.levelDimensions[1]*50))
        playerPos = (self.player.pos[0]*50,self.player.pos[1]*50)
        for pos in rayList:
            pygame.draw.line(self.screen,(255,0,0), playerPos,pos)
        pygame.draw.line(self.screen, (0,255,0),playerPos, (int(self.player.pos[0]*50+self.player.absVel[0]*50),int(self.player.pos[1]*50+self.player.absVel[1]*50)))
        pygame.draw.line(self.screen, (0,0,255), playerPos, (playerPos[0]+100*np.cos(self.player.cameraAngle),playerPos[1]+100*np.sin(self.player.cameraAngle)))
        print(thing)
        print(self.player.pos, self.player.cameraAngle*(180/np.pi))
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
    
    def raycast(self, angle, beta, x, y):
        rayList = []
        # print(angle)
        # ray-casting
        verticalHit = False
        verticalHitPos = None
        verticalHitWall = None
        horizontalHit = False
        horizontalHitPos = None
        horizontalHitWall = None
    
        # ***Vertical intersections*** #
        if angle < (np.pi / 2) or angle > ((3 * np.pi) / 2):
            dx = 1
            x1 = int(x) + dx
        else:
            dx = -1
            x1 = int(x)
        dy = 1 / np.tan(-(np.pi / 2) + angle)###
    
        y1 = (x - x1) * np.tan(-angle) + y
    
        currentx, currenty = x1, y1
        if dx == 1:  # ray going right
            for vertical in range(20):
                if not (0 < currentx < (self.levelDimensions[0])):
                    break
                elif not (0 < currenty < (self.levelDimensions[1])):
                    break
                square = self.level[int(currenty), currentx]
                if square != self.groundChar:
                    # print("vertical hit")
                    verticalHitPos = (currentx, currenty)
                    verticalHitWall = self.wallType[square]
                    verticalHit = True
                    rayList.append((verticalHitPos[0] * 50, verticalHitPos[1] * 50))
                    break
                else:
                    currentx += dx
                    currenty += dy
                pygame.draw.line(self.screen, (0,255,255),(self.player.pos[0]*50,self.player.pos[1]*50), (currentx*50,currenty*50))
                print("done")
                pygame.time.wait(100)
                pygame.display.update()
        else:  # going left
            for vertical in range(20):
                if not (0 < currentx < (self.levelDimensions[0])):
                    break
                elif not (0 < currenty < (self.levelDimensions[1])):
                    break
                square = self.level[int(currenty), (currentx - 1)]
                if square != self.groundChar:
                    # print("vertical hit")
                    verticalHitPos = (currentx, currenty)
                    verticalHitWall = self.wallType[square]
                    verticalHit = True
                    rayList.append((verticalHitPos[0] * 50, verticalHitPos[1] * 50))
                    break
                else:
                    currentx += dx
                    currenty += dy
                pygame.draw.line(self.screen, (0, 255, 255), (self.player.pos[0] * 50, self.player.pos[1] * 50),
                                 (currentx * 50, currenty * 50))
                print("done")
                pygame.time.wait(100)
                pygame.display.update()
        
        pygame.display.update()
        pygame.time.wait(100)
        # ***Horizontal Intersections*** #
        if angle < np.pi:
            dy = -1
            y1 = int(y)
        else:
            dy = 1
            y1 = int(y) + dy
        dx = (-dy) / np.tan(angle)
        x1 = (y - y1) / np.tan(angle) + x
        currentx, currenty = x1, y1
        if dy == 1:  # ray going down
            for horizontal in range(20):
                if not (0 < currentx < (self.levelDimensions[0])):
                    break
                elif not (0 < currenty < (self.levelDimensions[1])):
                    break
                square = self.level[currenty, int(currentx)]
                if square != self.groundChar:
                    # print("horizontal hit")
                    horizontalHitPos = (currentx, currenty)
                    horizontalHitWall = self.wallType[square]
                    horizontalHit = True
                    rayList.append((horizontalHitPos[0] * 50, horizontalHitPos[1] * 50))
                    break
                else:
                    currentx += dx
                    currenty += dy
                pygame.draw.line(self.screen, (0, 255, 0), (self.player.pos[0] * 50, self.player.pos[1] * 50),
                                 (currentx * 50, currenty * 50))
                print("done")
                pygame.time.wait(100)
                pygame.display.update()
        else:  # ray going up
            for horizontal in range(20):
                if not (0 < currentx < (self.levelDimensions[0])):
                    break
                elif not (0 < currenty < (self.levelDimensions[1])):
                    break
                square = self.level[currenty - 1, int(currentx)]
                if square != self.groundChar:
                    # print("horizontal hit")
                    horizontalHitPos = (currentx, currenty)
                    horizontalHitWall = self.wallType[square]
                    horizontalHit = True
                    rayList.append((horizontalHitPos[0] * 50, horizontalHitPos[1] * 50))
                    break
                else:
                    currentx += dx
                    currenty += dy
                pygame.draw.line(self.screen, (0, 255, 0), (self.player.pos[0] * 50, self.player.pos[1] * 50),
                                 (currentx * 50, currenty * 50))
                print("done")
                pygame.time.wait(100)
                pygame.display.update()
    
        if verticalHit and horizontalHit:
            if dx < 0:
                if horizontalHitPos[0] < verticalHitPos[0]:
                    viewDistance = np.sqrt((x - verticalHitPos[0]) ** 2 + (y - verticalHitPos[1]) ** 2)

                    # section = verticalHitWall.getTexture(verticalHitPos[1] % 1)
                    # section = pygame.transform.scale(section, ())
                else:
                    viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
            else:
                if horizontalHitPos[0] < verticalHitPos[0]:
                    viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
                
                    # section = verticalHitWall.getTexture(verticalHitPos[1] % 1)
                    # section = pygame.transform.scale(section, ())
                else:
                    viewDistance = np.sqrt((x - verticalHitPos[0]) ** 2 + (y - verticalHitPos[1]) ** 2)
    
        elif verticalHit:
            viewDistance = np.sqrt((x - verticalHitPos[0]) ** 2 + (y - verticalHitPos[1]) ** 2)
    
        elif horizontalHit:
            viewDistance = np.sqrt((x - horizontalHitPos[0]) ** 2 + (y - horizontalHitPos[1]) ** 2)
        else:
            viewDistance = None
        return viewDistance, rayList[0]
        
