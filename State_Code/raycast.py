import numpy as np
import pygame

class Ray:
    """
    >>> thing = Ray(1.001483136, 3.5,3.5,np.array([[" "," "," "," "," ","#"],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]])," ")
    >>> thing.horCast((thing.hx1, thing.hy1),10)
    """
    def __init__(self, angle, x, y, level, groundChar):
        """
        angle is measured in radians from the posative x-axis clockwise
        the point 0,0 is top-left
        """
        self.level = level
        self.groundChar = groundChar
        self.angle = angle
        self.x, self.y = x, y
        self.endX, self.endY = x, y
        self.vdx, self.vdy, self.vx1, self.vy1 = self.SetUpVerticalVars()(self)
        self.hdx, self.hdy, self.hx1, self.hy1 = self.SetUpHorizontalVars()(self)
        self.endPos, self.hitWall = self.cast()
        self.length = np.sqrt((self.x - self.endPos[0]) ** 2 + (self.y - self.endPos[1]) ** 2)
    
    def cast(self, searchDepth=100):
        vertEndpos, vertWall = self.vertCast((self.vx1, self.vy1), searchDepth)
        horEndpos, horWall = self.horCast((self.hx1, self.hy1), searchDepth)
        if abs(vertEndpos[0]-self.x) > abs(horEndpos[0]-self.x):
            if horWall != self.groundChar:
                return horEndpos, horWall
            else:
                return vertEndpos, vertWall
        else:
            if vertWall != self.groundChar:
                return vertEndpos, vertWall
            else:
                return horEndpos, horWall
        # return (vertEndpos, horEndpos)[abs(vertEndpos[0]-self.x) > abs(horEndpos[0]-self.x)]
        # ^keeping this for posterity

    def vertCast(self, rayPos, searchDepth):
        """
        :param rayPos: the current coordinate of the end of the ray
        :param searchDepth: how far to check before stopping
        :return:
        
        >>> thing = Ray(np.pi/4, 1.5, 1.4, np.array([["#","#","#"],["#"," ","#"],["#","#","#"]])," ")
        >>> tra = thing.vertCast((thing.vx1,thing.vy1), 10)
        >>> ((tra[0][0], np.round(tra[0][1], decimals=1)), tra[1])# doctest: +ELLIPSIS
        ((2, 0.900...), '#')
        
        >>> thing = Ray(5*np.pi/4, 2.5, 1.4, np.array([["#","#","#","#"],["#"," "," ","#"],["#"," "," ","#"],["#","#","#","#"]])," ")
        >>> tra = thing.vertCast((thing.vx1,thing.vy1), 10)
        >>> ((tra[0][0], round(tra[0][1], 1)), tra[1])# doctest: +ELLIPSIS
        ((1, 2.89...), '#')
        """
        if searchDepth < 0:
            return rayPos, self.groundChar
        
        try:
            wall = self.level[self.getVerticalWallIndex(rayPos)]
        except IndexError:
            return rayPos, self.groundChar
        
        if wall != self.groundChar:
            return rayPos, wall
        else:
            newPos = (rayPos[0]+self.vdx, rayPos[1]+self.vdy)
            return self.vertCast(newPos, searchDepth-1)
            
    def horCast(self, rayPos, searchDepth):
        """
        :param rayPos:
        :param searchDepth:
        :return:
        
        >>> thing = Ray(np.pi/4, 1.4, 1.5, np.array([["#","#","#"],["#"," ","#"],["#","#","#"]])," ")
        >>> tra = thing.horCast((thing.hx1,thing.hy1), 10)
        >>> ((round(tra[0][0],1), round(tra[0][1], 1)), tra[1])# doctest: +ELLIPSIS
        ((1.89..., 1), '#')
        
        >>> thing = Ray(5*np.pi/4, 2.6, 1.5, np.array([["#","#","#","#"],["#"," "," ","#"],["#"," "," ","#"],["#","#","#","#"]])," ")
        >>> tra = thing.horCast((thing.hx1,thing.hy1), 10)
        >>> ((round(tra[0][0],1), round(tra[0][1], 1)), tra[1])# doctest: +ELLIPSIS
        ((1.1..., 3), '#')
        """
        if searchDepth < 0:
            return rayPos, self.groundChar
        
        try:
            wall = self.level[self.getHorizontalWallIndex(rayPos)]
        except IndexError:
            return rayPos, self.groundChar
            

        if wall != self.groundChar:
            return rayPos, wall
        else:
            newPos = (rayPos[0] + self.hdx, rayPos[1] + self.hdy)
            return self.horCast(newPos, searchDepth - 1)
        
    def getVerticalWallIndex(self, pos):
        """
        :param pos:
        :return:
        
        >>> Ray(np.pi/4, 1.5, 1.6, np.array([[""]])," ").getVerticalWallIndex((2, 1.1))
        (1, 2)
        >>> Ray(5*np.pi/4, 1.5, 1.4, np.array([[""]])," ").getVerticalWallIndex((1, 1.9))
        (1, 0)
        """
        if self.vdx < 0:
            return int(pos[1]), int(pos[0])-1
        else:
            return int(pos[1]), int(pos[0])
        
    def getHorizontalWallIndex(self, pos):
        """
        :param pos:
        :return:
        
        >>> Ray(np.pi/4, 1.4, 1.5, np.array([[""]])," ").getHorizontalWallIndex((1.9, 1))
        (0, 1)
        >>> Ray(5*np.pi/4, 1.6, 1.5, np.array([[""]])," ").getHorizontalWallIndex((1.1, 2))
        (2, 1)
        """
        if self.hdy < 0:
            return int(pos[1]) - 1, int(pos[0])
        else:
            return int(pos[1]), int(pos[0]),
            
    class SetUpVerticalVars:
        """
        >>> test = Ray.SetUpVerticalVars()(Ray(np.pi/4, 1.5, 1.5, np.array([[""]])," "))
        >>> [round(a) for a in test]
        [1, -1.0, 2, 1.0]
        """
        def __call__(self, rayObj):
            vdx = self.getVerticaldx(rayObj.angle)
            vdy = self.getVerticaldy(rayObj.angle, vdx)
            vx1 = self.getVerticalx1(vdx, rayObj.x)
            vy1 = self.getVerticaly1(rayObj.x, rayObj.y, vx1, rayObj.angle)
            return vdx, vdy, vx1, vy1
        @staticmethod
        def getVerticaldx(angle):
            """
            :return:
            >>> Ray.SetUpVerticalVars.getVerticaldx(np.pi/4)
            1
            >>> Ray.SetUpVerticalVars.getVerticaldx(0)
            1
            >>> Ray.SetUpVerticalVars.getVerticaldx(5*np.pi/4)
            -1
            >>> Ray.SetUpVerticalVars.getVerticaldx(np.pi)
            -1
            """
            
            if (np.pi / 2) < angle < ((3 * np.pi) / 2):
                return -1
            else:
                return 1
    
        @staticmethod
        def getVerticaldy(angle, vdx):
            """
            :param vdx:
            :param angle:
            :return:
            
            >>> np.round(Ray.SetUpVerticalVars.getVerticaldy(np.pi/4, 1), 6)  # doctest: +ELLIPSIS
            -1.0...
            >>> np.round(Ray.SetUpVerticalVars.getVerticaldy(3*np.pi/4, -1), 6)  # doctest: +ELLIPSIS
            -1.0...
            >>> np.round(Ray.SetUpVerticalVars.getVerticaldy(5*np.pi/4, -1), 6)  # doctest: +ELLIPSIS
            1.0...
            >>> np.round(Ray.SetUpVerticalVars.getVerticaldy(7*np.pi/4, 1), 6)  # doctest: +ELLIPSIS
            1.0...
            
            #>>> Ray.SetUpVerticalVars.getVerticaldy()
            """
            return -vdx * np.tan(angle)
            
        @staticmethod
        def getVerticalx1(vdx, x):
            """
            :param vdx:
            :return:
            
            >>> Ray.SetUpVerticalVars.getVerticalx1(1, 1.4)
            2
            >>> Ray.SetUpVerticalVars.getVerticalx1(-1, 1.4)
            1
            """
            if vdx < 0:
                return int(x)
            else:
                return int(x) + 1
        
        @staticmethod
        def getVerticaly1(x, y, x1, angle):
            """
            :param x:
            :param y:
            :param x1:
            :param angle:
            :return:
            
            >>> np.round(Ray.SetUpVerticalVars.getVerticaly1(1.5, 1.5, 2, np.pi/4))
            1.0
            >>> np.round(Ray.SetUpVerticalVars.getVerticaly1(1.5, 1.5, 2, 7*np.pi/4))
            2.0
            >>> np.round(Ray.SetUpVerticalVars.getVerticaly1(1.5, 1.5, 1, 3*np.pi/4))
            1.0
            >>> np.round(Ray.SetUpVerticalVars.getVerticaly1(1.5, 1.5, 1, 5*np.pi/4))
            2.0
            """
            return y + (x - x1) * np.tan(angle)
    
    
    class SetUpHorizontalVars:
        """
        >>> Ray.SetUpHorizontalVars()(Ray(np.pi/4, 1.5, 1.5, np.array([[""]]), " ")) # doctest: +ELLIPSIS
        (1.0..., -1, 2.0, 1)
        """
        def __call__(self, rayObj):
            dy = self.getHorizontaldy(rayObj.angle)
            dx = self.getHorizontaldx(rayObj.angle, dy)
            y1 = self.getHorizontaly1(dy, rayObj.y)
            x1 = self.getHorizontalx1(rayObj.x, rayObj.y, y1, rayObj.angle)
            return (dx, dy, x1, y1)
        
        @staticmethod
        def getHorizontaldx(angle, dy):
            """
            :param angle:
            :param dy:
            :return:
            
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontaldx(np.pi/4, -1))
            1.0
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontaldx(7*np.pi/4, 1))
            1.0
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontaldx(3*np.pi/4, -1))
            -1.0
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontaldx(5*np.pi/4, 1))
            -1.0
            """
            return -dy / np.tan(angle)
        
        @staticmethod
        def getHorizontaldy(angle):
            """
            :param angle:
            :return:
            
            >>> Ray.SetUpHorizontalVars.getHorizontaldy(np.pi/4)
            -1
            >>> Ray.SetUpHorizontalVars.getHorizontaldy(3*np.pi/4)
            -1
            >>> Ray.SetUpHorizontalVars.getHorizontaldy(5*np.pi/4)
            1
            >>> Ray.SetUpHorizontalVars.getHorizontaldy(7*np.pi/4)
            1
            """
            if angle < np.pi:
                return -1
            else:
                return 1
        
        @staticmethod
        def getHorizontalx1(x, y, y1, angle):
            """
            :param x:
            :param y:
            :param y1:
            :param angle:
            :return:
            
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontalx1(1.5, 1.5, 1, np.pi/4))
            2.0
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontalx1(1.5, 1.5, 1, 3*np.pi/4))
            1.0
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontalx1(1.5, 1.5, 2, 5*np.pi/4))
            1.0
            >>> np.round(Ray.SetUpHorizontalVars.getHorizontalx1(1.5, 1.5, 2, 7*np.pi/4))
            2.0
            """
            return (y - y1) / np.tan(angle) + x
        
        @staticmethod
        def getHorizontaly1(hdy, y):
            """
            :param hdy:
            :param y:
            :return:
            
            >>> Ray.SetUpHorizontalVars.getHorizontaly1(-1, 1.5)
            1
            >>> Ray.SetUpHorizontalVars.getHorizontaly1(1, 1.5)
            2
            """
            if hdy < 0:
                return int(y)
            else:
                return int(y) + 1
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
