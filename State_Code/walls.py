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
        
    def getTexture(self, dist):
        """
        :param dist: a float representing the distance from the lower coordinate grid line
        :return: the texture segment corresponding to the distance specified
        """
        return self._textureSections[int((64 * dist) / self._columnWidth)]
    
    def handleCollision(self, player):
        player.demove()
        
