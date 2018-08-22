import numpy as np

class ray:
    
    def __init__(self, angle, x, y, level):
        """
        angle is measured in radians from the posative x-axis clockwise
        the point 0,0 is top-left
        """
        self.level = level
        self.angle = angle
        self.x, self.y = x, y
        self.endX, self.endY = x, y
    
    def cast(self, searchDepth=19):
        vdx, vdy, vx1, vy1 = self.SetUpVerticalVars(self)
        vertEndpos = self.vertCast(searchDepth)
        horEndpos = self.horCast(searchDepth)
        if abs(vertEndpos[0]-self.x) > abs(horEndpos[0]-self.x):
            return horEndpos
        else:
            return vertEndpos
        #return (vertEndpos, horEndpos)[abs(vertEndpos[0]-self.x)>abs(horEndpos[0]-self.x)]

    def vertCast(self, x1, y1, dx, dy, searchDepth):
        pass

    def horCast(self, x1, y1, dx, dy, searchDepth):
        pass
    
    class SetUpVerticalVars:
        def __call__(self, rayObj):
            vdx = self.getVerticaldx(rayObj.angle)
            vdy = self.getVerticaldy(rayObj.angle, vdx)
            vx1 = self.getVerticalx1(vdx)
            vy1 = self.getVerticaly1(rayObj.x, rayObj.y, vx1, rayObj.angle)
            return vdx, vdy, vx1, vy1
        @staticmethod
        def getVerticaldx(angle):
            """
            :return:
            >>> ray.SetUpVerticalVars.getVerticaldx(np.pi/4)
            1
            >>> ray.SetUpVerticalVars.getVerticaldx(0)
            1
            >>> ray.SetUpVerticalVars.getVerticaldx(5*np.pi/4)
            -1
            >>> ray.SetUpVerticalVars.getVerticaldx(np.pi)
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
            
            >>> np.round(ray.SetUpVerticalVars.getVerticaldy(np.pi/4, 1), 6)  # doctest: +ELLIPSIS
            1.0...
            >>> np.round(ray.SetUpVerticalVars.getVerticaldy(3*np.pi/4, -1), 6)  # doctest: +ELLIPSIS
            1.0...
            >>> np.round(ray.SetUpVerticalVars.getVerticaldy(5*np.pi/4, -1), 6)  # doctest: +ELLIPSIS
            -1.0...
            >>> np.round(ray.SetUpVerticalVars.getVerticaldy(7*np.pi/4, 1), 6)  # doctest: +ELLIPSIS
            -1.0...
            """
            return vdx / np.tan(angle)
            
        @staticmethod
        def getVerticalx1(vdx):
            if vdx < 0:
                return int(self.x)
            else:
                return int(self.x) + 1
        
        @staticmethod
        def getVerticaly1(x, y, x1, angle):
            return y - (x - x1) * np.tan(angle)
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
