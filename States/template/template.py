import abc

class State(abc.ABC):
    """ 
    an base class used as a marker for state classes 
    """

    def __init__(self, screen, nextState):
        self.nextState = nextState
        self.quit = False
        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_size()

    @abc.abstractmethod
    def startup(self, persistentVar):
        """
        called when the state becomes active,
        persistentVar should be a list
        """
        pass

    @abc.abstractmethod
    def exit(self):
        """
        called when the state is switched from this state,
        should return the persistentVar
        """
        pass

    @abc.abstractmethod
    def draw(self,screen):
        """
        draws all the necessary things to the screen
        """
        pass

    @abc.abstractmethod
    def update(self,dt):
        """
        provides game logic
        dt is the delay time generated from clock.tick()
        """
        pass

    @abc.abstractmethod
    def getEvent(self,event):
        """
        handles a single pygame event passed to it by the controll class
        """
        pass
