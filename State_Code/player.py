import numpy as np


class Player:
    
    def __init__(self, speed, pos, cameraAngle):
        self.speed = speed
        self.pos = pos
        self._cameraAngle = cameraAngle
        
        self.cameraVel = 0
        self.absVel = np.array([0, 0])
        self._relVel = np.array([0, 0])
        
    @property
    def intPos(self):
        return [int(self.pos[0]), int(self.pos[1])]
    
    @property
    def relVel(self):
        return self._relVel
    
    @relVel.setter
    def relVel(self, value):
        self._relVel = value
        self.absVel = self.rotateVector(self._relVel, self.cameraAngle)
    
    @property
    def cameraAngle(self):
        return self._cameraAngle
    
    @cameraAngle.setter
    def cameraAngle(self, value):
        self._cameraAngle = value % (np.pi*2)
        self.absVel = self.rotateVector(self.relVel, self.cameraAngle)
        
    def move(self):
        self.pos += self.vel
        
    def demove(self):
        self.pos -= self.vel
        
    def turn(self):
        self.cameraAngle += self.cameraVel

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
