import numpy as np


class Player:
    
    def __init__(self, speed, pos, cameraAngle):
        self.speed = speed
        self.pos = pos
        self._cameraAngle = cameraAngle
        
        self.cameraVel = 0
        self._absVel = np.array([0, 0])
        self._relVel = np.array([0, 0])
        
    @property
    def intPos(self):
        return [int(self.pos[0]), int(self.pos[1])]
    
    @property
    def relVel(self):
        """
        this is the player's velocity relative to the camera angle
        """
        return self._relVel
    
    @relVel.setter
    def relVel(self, value):
        """
        updates the absolute velocity when relVel changes
        """
        self._relVel = value
        self._absVel = self.rotateVector(self._relVel, self.cameraAngle)
    
    @property
    def cameraAngle(self):
        return self._cameraAngle
    
    @cameraAngle.setter
    def cameraAngle(self, value):
        """
        updates the absolute velocity when the camera angle changes
        """
        self._cameraAngle = value % (2*np.pi)  # angle wrapping
        self._absVel = self.rotateVector(self.relVel, self.cameraAngle)
        
    def move(self):
        self.pos += self._absVel
        
    def demove(self):
        self.pos -= self._absVel
        
    def turn(self):
        self.cameraAngle += self.cameraVel

    @staticmethod
    def rotateVector(vector, angle):
        """
        returns a numpy array that is vector rotated anticlockwise by angle radians

        >>> [round(a) for a in Player.rotateVector(np.array([1,0]), np.pi/2)]
        [0.0, -1.0]

        >>> [round(a) for a in Player.rotateVector(np.array([0,1]), np.pi/2)]
        [1.0, 0.0]

        >>> [round(a) for a in Player.rotateVector(np.array([0,-1]), np.pi/2)]
        [-1.0, -0.0]

        >>> [round(a,1) for a in Player.rotateVector(np.array([0,-1]), np.pi/4)]
        [-0.7, -0.7]
        """
        sinTheta = np.sin(-angle)
        cosTheta = np.cos(-angle)
        newX = (cosTheta * vector[0]) - (sinTheta * vector[1])
        newY = (sinTheta * vector[0]) + (cosTheta * vector[1])
        return np.array([newX, newY])

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
