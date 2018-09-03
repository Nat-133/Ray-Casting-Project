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
    wallType = {"#":walls.Wall("test_wall.png"), "E":walls.NextLevelDoor("exit_wall.png")}
    
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
        self.timerFont = pygame.font.Font(None, 100)
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
            self.player = player.Player(1, np.array([1.5, 1.5]), (7 * np.pi / 4))
        else:
            self.startTime = time.time()
            
    def exit(self):
        self.extraTime += time.time() - self.startTime
        return self.persistentVar
    
    def draw(self):
        """
        ray casting
        
        :return:
        """
        rayList =[]
        self.screen.fill((255,255,255))
        angleIncrement = self.fov/self.screenRes[0]
        columnWidth = int(self.screenWidth/self.screenRes[0])
        angle = (self.player.cameraAngle + (self.fov / 2) + 0.0000001) % (2*np.pi)
        
        beta = int(self.fov/2) + 0.0000001
        x, y = self.player.pos
        bugAngleList = []
        for column in range(int(self.screenRes[0])):
            ray = raycast.Ray(angle, x, y, self.level, self.groundChar)
            rayList.append(ray)
            viewDistance = ray.length
            #print(np.degrees(angle), np.degrees(angle - self.player.cameraAngle))
            actualDistance = viewDistance * np.cos(angle - self.player.cameraAngle)
            # actualDistance = viewDistance * np.cos(beta)
            hitWall = self.wallType[ray.hitWall]
            sliceTexture = hitWall.getTexture(ray.endPos)
            topyPos = (self.screenHeight - (1 / actualDistance) * self.screenHeight * 1)/2
            wallHeight = int((1 / actualDistance) * self.screenHeight * 1)
            try:
                sliceTexture = pygame.transform.scale(sliceTexture, (columnWidth, wallHeight))
                self.screen.blit(sliceTexture, (column * columnWidth, topyPos))
            except pygame.error:
                # this is because transform.scale has a limit, when you get too close to the wall, the image
                # slices get toooooooo large
                pygame.draw.rect(self.screen, (actualDistance * 5, actualDistance * 5, actualDistance * 5),
                                 pygame.Rect(column * columnWidth, 0, columnWidth, self.screenHeight))
            
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
            self.nextState = self.wallType[wall].handleCollision(self.player, self)
            if self.nextState != self.id:
                self.persistentVar.update(self.wallType[wall].nextStateArgs)
        self.player.turn()
        
    def getEvent(self, event):
        """
        movement and camera rotation to change velocity
        pause
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.relVel = np.array([0.05, 0])
            elif event.key == pygame.K_s:
                self.player.relVel = np.array([-0.05, 0])
            elif event.key == pygame.K_a:
                self.player.cameraVel = 0.05
            elif event.key == pygame.K_d:
                self.player.cameraVel = -0.05
            elif event.key == pygame.K_ESCAPE:
                self.nextState = "pause"
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.player.relVel = np.array([0, 0])
            elif event.key == pygame.K_s:
                self.player.relVel = np.array([0, 0])
            elif event.key == pygame.K_a:
                self.player.cameraVel = 0
            elif event.key == pygame.K_d:
                self.player.cameraVel = 0
