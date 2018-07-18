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
        self.levelNum = 1
        self.level = np.array([])
        self.levelFile = "level_1.txt"
        self.startTime = time.time()
        self.extraTime = 0
        
        self.player = player.Player(1, np.array([1.5, 1.5]), 0)
        self.fov = 90
        

    def startup(self, persistentVar):
        """
        ### called when the state becomes active
        :param persistentVar: should be a a list in the form [restart, level number]
        :return:
        """
        self.nextState = self.id
        self.persistentVar = persistentVar
        if not self.persistentVar[0]:
            self.extraTime = 0
            self.startTime = time.time()
            self.levelNum = self.persistentVar[0]
            self.levelFile = f"level_{self.levelNum}.txt"
            with open(os.path.relpath("..//Levels//{self.levelFile}"), "r") as f:
                self.level = json.loads(f.read())
            self.startTime = time.time()
        else:
            self.extraTime = time.time() - self.startTime
            self.startTime = time.time()
            
    def exit(self):
        return []
    
    def draw(self):
        """
        ray casting
        
        :return:
        """
        pass
    
    def update(self):
        """
        changes position and camera angle based on velocities
        also collisions
        :return:
        """
        self.player.move()
        wall = self.level[x for x in reverse(self.player.intPos)]
        if wall != self.groundChar:
            self.wallType[wall].handleCollision(self.player)
        
    
    def getEvent(self, event):
        """
        movement and camera rotation to change velocity
        pause
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.relVel = np.array([1,0])
            elif event.key == pygame.K_s:
                self.player.relVel = np.array([-1,0])
            elif event.key == pygame.K_a:
                self.player.cameraVel = 1
            elif event.key == pygame.K_d:
                self.player.cameraVel = -1
