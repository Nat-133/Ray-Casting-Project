import os, sys
import json
import time
import pygame
import numpy as np
from math import ceil

from States import template
from State_Code import walls
from State_Code import player
from State_Code import raycast

class Gameplay(template.State):
    groundChar = " "
    columnWidth = 1  # the width of the wall slices in pixels
    wallType = {"#" : walls.Wall("Stone_brick_wall.png", columnWidth),
                "B" : walls.Wall("Redbrick_wall.png", columnWidth),
                "M" : walls.Wall("Mossy_wall.png", columnWidth),
                "C" : walls.Wall("Cave_wall.png", columnWidth),
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
        
        self.player = player.Player(0.05, np.array([1.5, 1.5]), (7*np.pi/4))
        self.fov = np.pi/3

        self.timerFont = pygame.font.Font(None,50)
        self.timerColour = (0, 200, 0)

        self.mouseSensitivity = 0.01
        
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
            try:
                with open(os.path.relpath(f"Levels//{self.levelFile}"), "r") as f:
                    self.level = np.array(json.loads(f.read()))  # loads the level into a numpy array
            except (json.decoder.JSONDecodeError, FileNotFoundError):
                self.level = np.array([["#","#","#"],
                                       ["#"," ","#"],
                                       ["#","#","#"]])
            self.levelDimensions = self.level.shape
            self.player = player.Player(0.05, np.array([1.5, 1.5]), (7 * np.pi / 4))

        self.startTime = time.time()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        #^ affixes the curser to the window
        pygame.mouse.get_rel()
        #^ resets the relative position of the mouse
            
    def exit(self):
        self.player.sprint = False
        self.extraTime = self.getTime()
        self.persistentVar["time"] = self.extraTime
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
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
                sliceTexture = hitWall.getTexture(ray.endPos)
                currentSliceSize = sliceTexture.get_size()
                wallHeight = int((1 / actualDistance) * self.screenHeight)  # the size of the scaled full texture
                textureScaleFactor = wallHeight / currentSliceSize[1]
                newSliceHeight = min(currentSliceSize[1], ceil(self.screenHeight/textureScaleFactor))
                newSliceTopy = int((currentSliceSize[1]-newSliceHeight)/2)  
                newSliceHeight = currentSliceSize[1]-2*newSliceTopy  # makes the topy and height rounding consistent
                #^ the height of the texture that will be scaled up
                sliceSection = pygame.Rect(0, newSliceTopy,
                                            self.columnWidth, newSliceHeight)
                textureSection = sliceTexture.subsurface(sliceSection)
                     
                if newSliceHeight > 2:  # if the slice is larger than 2 pixels
                    scaledSectionHeight = int(newSliceHeight*textureScaleFactor)
                    sliceTexture = pygame.transform.scale(textureSection, (self.columnWidth, scaledSectionHeight))
                    #^ scales the cropped texture to the correct size

                    topyPos = (self.screenHeight-scaledSectionHeight)//2
                    self.screen.blit(sliceTexture, (column * self.columnWidth, topyPos))
                else:
                    # allows the player to get as close to the wall as they like
                    colour = textureSection.get_at((0,0))
                    pygame.draw.rect(self.screen, colour, pygame.Rect(column * self.columnWidth, 0,
                                                 self.columnWidth, self.screenHeight))
            
            angle = (angle - angleIncrement) % (2 * np.pi)

        # draws the player's time
        timeText = self.timerFont.render(f"{round(self.getTime(),3)}", True, self.timerColour)
        self.screen.blit(timeText, (0,0))
        
    
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
        self.player.cameraAngle += pygame.mouse.get_rel()[0] * -self.mouseSensitivity
        
    def getEvent(self, event):
        """
        movement and camera rotation to change velocity
        pause
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.player.relDirection = np.array([1, 0])
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.player.relDirection = np.array([-1, 0])
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.cameraVel = 0.05
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.cameraVel = -0.05
            elif event.key == pygame.K_f or event.key == pygame.K_LSHIFT:
                self.player.sprint = True
            elif event.key == pygame.K_ESCAPE:
                self.nextState = "pause"
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.player.relDirection = np.array([0, 0])
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.player.relDirection = np.array([0, 0])
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.cameraVel = 0
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.cameraVel = 0
            elif event.key == pygame.K_f or event.key == pygame.K_LSHIFT:
                self.player.sprint = False

    def getTime(self):
        return time.time() - self.startTime + self.extraTime
