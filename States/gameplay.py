import os, sys
import json
import time
import pygame
import numpy as np
import template.template as template


class Gameplay(template.State):

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
        self.level = []
        self.levelFile = "level_1.txt"
        self.startTime = time.time()
        self.extraTime = 0
        
        self.speed = 1 # the speed of the player when moving
        self.pos = np.array([0, 0])
        self.vel = np.array([0, 0])
        self._cameraAngle = 0
        self.rotationVel = 0
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
        pass
    
    def getEvent(self, event):
        """
        movement and camera rotation to change velocity
        pause
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.vel = self.rotateVector([1, 0], self.cameraAngle)
            elif event.key == pygame.K_s:
                self.vel = self.rotateVector(([-1, 0], self.cameraAngle))
            elif event.key == pygame.K_a:
                self.rotationVel = 1
            elif event.key == pygame.K_d:
                self.rotationVel = -1
    @staticmethod
    def rotateVector(vector, angle):
        """
        :param vector: an array like object with dimensions 2,1
        :param angle: an angle in radians
        :return: a numpy array which is the original vector rotated anticlockwise by 'angle' radians
        """
        sinTheta = np.sin(angle)
        cosTheta = np.cos(angle)
        newX = (cosTheta * vector[0]) - (sinTheta * vector[1])
        newY = (sinTheta * vector[0]) + (cosTheta * vector[1])
        return np.array([newX, newY])
    
    @property
    def cameraAngle(self):
        return self._cameraAngle
    
    @cameraAngle.setter
    def cameraAngle(self, value):
        self._cameraAngle = value % (np.pi*2)
