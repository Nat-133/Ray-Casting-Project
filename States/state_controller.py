import pygame

class StateController:

    def __init__(self):
        pygame.init()
        self.screenWidth = 500
        self.screenHeight = 500
        self.screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))

        self.quit = False
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.stateDict = {"menu":1,
                          "level select":2,
                          "gameplay":3,
                          "pause":4}
        self.activeState = self.stateDict["menu"]
        self.persistentVar = False

    def gameloop(self):
        """
        the main loop for the game, most of the game's runtime will be spent in here
        Calls the aciveState's getEvent (for event handling)
        Calls the activeSate's update   (for game logic)
        Calls the aciveState's draw     (to draw everything to the screen)
        """
        while not self.quit:
            dt = self.clock.tick(self.FPS)
            nextState = self.stateDict[self.activeState.nextState]

            if self.activeState == nextState: # if the activeState is unchanged
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.activeState.exit()
                        self.quit = True
                    self.activeState.getEvent(event)
                self.activeSate.update()
                self.activeState.draw()

                pygame.display.update()
            else: # if the activeState needs to be changed
                self.persistentVar = self.activeState.exit()
                self.activeState = nextState
                self.activeState.startup(self.persistentVar)