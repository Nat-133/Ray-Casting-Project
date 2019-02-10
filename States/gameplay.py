import os, sys
import json
import time
import pygame
import numpy as np

from States import template
from State_Code import walls
from State_Code import player
from State_Code import raycast

class Gameplay(template.State):
    groundChar = " "
    columnWidth = 1  # the width of the wall slices in pixels
    wallType = {"#" : walls.Wall("test_wall.png", columnWidth),
                "B" : walls.Wall("test_wall_2.png", columnWidth),
                "E" : walls.NextLevelDoor("exit_wall.png", columnWidth)}
    
    def __init__(self, screen, identifier="gameplay"):
        super().__init__(screen, identifier)
        self.screenRes = (int(self.screenWidth/self.columnWidth), self.screenHeight)  # the resolution used when drawing the walls
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
        called when the state becomes active
        """
        self.nextState = self.id
        self.persistentVar = persistentVar
        if self.persistentVar["restart"]:
            self.extraTime = 0
            self.levelNum = self.persistentVar["levelNum"]
            self.levelFile = f"level_{self.levelNum}.txt"
            with open(os.path.relpath(f"Levels//{self.levelFile}"), "r") as f:
                self.level = np.array(json.loads(f.read()))  # loads the level into a numpy array
            self.levelDimensions = self.level.shape
            self.player = player.Player(1, np.array([1.5, 1.5]), (7 * np.pi / 4))

        self.startTime = time.time()
            
    def exit(self):
        self.extraTime += time.time() - self.startTime
        return self.persistentVar
    
    def draw(self):
        """
        ray casting for every pixle collumn
        """
        self.screen.fill((75,75,75))
        floorRect = pygame.Rect(0, int(self.screenHeight/2), self.screenWidth, int(self.screenHeight/2))
        pygame.draw.rect(self.screen, (25,25,25), floorRect)
        angleIncrement = self.fov/self.screenRes[0]
        angle = (self.player.cameraAngle + (self.fov / 2) + 0.0000001) % (2*np.pi)
        
        x, y = self.player.pos
        bugAngleList = []
        for column in range(int(self.screenRes[0])):
            ray = raycast.Ray(angle, x, y, self.level, self.groundChar)
            viewDistance = ray.length
            actualDistance = viewDistance * np.cos(angle - self.player.cameraAngle)
            try:
                hitWall = self.wallType[ray.hitWall]
            except KeyError:
                pass
            else:
                topyPos = (self.screenHeight - (1 / actualDistance) * self.screenHeight * 1)/2
                wallHeight = int((1 / actualDistance) * self.screenHeight * 1)
                sliceTexture = hitWall.getTexture(ray.endPos)
                sliceTexture = pygame.transform.scale(sliceTexture, (self.columnWidth, wallHeight))
                self.screen.blit(sliceTexture, (column * self.columnWidth, topyPos))

            angle = (angle - angleIncrement) % (2 * np.pi)

            """
                try:
                    
                except pygame.error:
                    # this is because transform.scale has a limit, when you get too close to the wall, the image
                    # slices get toooooooo large
                    pygame.draw.rect(self.screen, (actualDistance * 5, actualDistance * 5, actualDistance * 5),
                                     pygame.Rect(column * columnWidth, 0, columnWidth, self.screenHeight))
            except KeyError:
                pass
            """
            
            
            
        
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
        """
        self.player.move()
        pos = self.player.intPos
        wall = self.level[pos[1], pos[0]]
        if wall != self.groundChar:  # if player is not in an empty square
            self.wallType[wall].handleCollision(self.player, self)  # calls the wall's collision method
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
                self.nextState = "menu"
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.player.relVel = np.array([0, 0])
            elif event.key == pygame.K_s:
                self.player.relVel = np.array([0, 0])
            elif event.key == pygame.K_a:
                self.player.cameraVel = 0
            elif event.key == pygame.K_d:
                self.player.cameraVel = 0
