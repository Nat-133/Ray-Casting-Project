import sys, os
import pygame
print('Path to module:', locals()['pygame'])

class Wall:
    """
    a class for defining a standard wall in the game
    """
    def __init__(self, textureFileName, columnWidth):
        self._fullTexture = pygame.image.load(os.path.relpath(f"Sprites//{textureFileName}"))
        self._textureSize = self._fullTexture.get_size()
        self._columnWidth = columnWidth
        self._textureSlices = [self._fullTexture.subsurface(x*self._columnWidth, 0, self._columnWidth, self._textureSize[1])
                               for x in range(self._textureSize[0]//self._columnWidth)]

    def handleCollision(self, player, state):
        player.demove()
  
    def getTexture(self, hitCoord):
        """
        hitCoord: a tuple representing the coordinates of a ray's hit position
        returns the texture segment corresponding to the distance specified
        """
        xDist = float(hitCoord[0] % 1)
        yDist = float(hitCoord[1] % 1)
        
        if xDist == 0:  # if the hit wall is vertical
            return self._textureSlices[int((self._textureSize[1] * yDist) / self._columnWidth)]
        else:
            return self._textureSlices[int((self._textureSize[0] * xDist) / self._columnWidth)]


class NextLevelDoor(Wall):
    """
    the wall type for the level end portal
    """
    def __init__(self, textureFile, columnWidth):
        super().__init__(textureFile, columnWidth)
        self.nextStateArgs = {"levelNum":1, "restart":True}
        
    def handleCollision(self, player, state):
        self.nextStateArgs.update({"levelNum":state.levelNum})
        state.persistentVar.update(self.nextStateArgs)
        state.nextState = "level complete"
