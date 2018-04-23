
class State:
    """ 
    an base class used as a marker for state classes 
    """

    def __init__(self,nextState):
        self.nextState = nextState
        self.quit = False

    def startup(self,persistentVar):
        """ called when the state becomes active, persistentVar should be a list """
        raise NotImplementedError (f"No startup method for {self.__class__.__name__} state")

    def exit(self):
        """ called when the state is switched from this state, should return the persistentVar """
        raise NotImplementedError (f"No exit method for {self.__class__.__name__} state")
        
    def draw(self,screen):
        """ draws all the necessary things to the screen """
        raise NotImplementedError (f"No draw method for {self.__class__.__name__} state")

    def update(self):
        """ provides game logic """
        raise NotImplementedError (f"No update method for {self.__class__.__name__} state")

    def getEvent(self,event):
        """ handles a single pygame event passed to it by the controll class """
        raise NotImplementedError (f"No event handling method for {self.__class__.__name__} state")
