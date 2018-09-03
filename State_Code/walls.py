import sys, os
import pygame
print('Path to module:', locals()['pygame'])

class Wall:
    """
    a class for defining a standard wall in the game
    """
    def __init__(self, textureFile):
        """
        :param textureFile: the file name of a 64x64px image file
        """
        self._fullTexture = pygame.image.load(os.path.relpath(f"..//Sprites//{textureFile}"))
        self._columnWidth = 4
        self._textureSections = [self._fullTexture.subsurface((x*self._columnWidth, 0, self._columnWidth, 64))
                                 for x in range(16)]
        
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
    
    def handleCollision(self, player, state):
        player.demove()
        return state.id


class NextLevelDoor(Wall):
    """
    the wall type for the level end portal
    """
    def __init__(self, textureFile):
        super().__init__(textureFile)
        self.nextStateArgs = {"levelNum":1, "restart":True}
        
    def handleCollision(self, player, state):
        self.nextStateArgs["levelNum"] = state.levelNum + 1
        return "level select"
