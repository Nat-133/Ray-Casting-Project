import sys, os
import pygame
print('Path to module:', locals()['pygame'])

class Wall:
    """
    a class for defining a standard wall in the game
    """
    def __init__(self, textureFileName):
        self._fullTexture = pygame.image.load(os.path.relpath(f"Sprites//{textureFileName}"))
        self._textureSize = self._fullTexture.get_size()
        self._columnWidth = 4
        self._textureSlices = [self._fullTexture.subsurface(x*self._columnWidth, 0, self._columnWidth, self._textureSize[1])
                               for x in range(self._textureSize[0]//self._columnWidth)]

    def handleCollision(self, player, state):
        player.demove()
  
    def getTexture(self, hitCoord):
        """
        :param: hitCoord: a tuple representing the coordinates of a ray's hit position
        :return: the texture segment corresponding to the distance specified
        """
        xDist = hitCoord[0] % 1
        yDist = hitCoord[1] % 1
        
        if xDist == 0:
            return self._textureSections[int((64 * yDist) / self._columnWidth)]
        else:
            return self._textureSections[int((64 * xDist) / self._columnWidth)]
    
    

class NextLevelDoor(Wall):
    """
    the wall type for the level end portal
    """
    def __init__(self, textureFile):
        super().__init__(textureFile)
        self.nextStateArgs = {"levelNum":1, "restart":True}
        
    def handleCollision(self, player, state):
        self.nextStateArgs.update({"levelNum":state.levelNum+1})
        state.persistentVar.update(self.nextStateArgs)
        state.nextState = "level select"
