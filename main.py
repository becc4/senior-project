# imports
import pygame

# constants
screen_X = 1280
screen_Y = 720

class main:
    def __init__(self):
        pygame.init()

        # (only) instances of other classes
        self.input_manager = inputs()
        self.graphic_manager = graphics(self.input_manager)

        # the levels of the game
        self.levels = [level_1()]
        self.curr_level = self.levels[0]

        # make the game run
        self.running = True
        self.game_loop()


    def game_loop(self):
        """
        make the game run
        will check if current_level is active
        """
        # basic graphics
        self.graphic_manager.start_graphics()

        # while game is running
        while self.running:
            # get events, before anything else (start of the game)
            self.input_manager.set_events()

            """EXIT CLAUSES"""
            # exit if there are no more levels
            if len(self.levels) <= 0:
                self.running = False
            
            # exit if the game manually ended
            if self.input_manager.is_exit():
                self.running = False            

"""
has no parameters, only returns. 
"""
class inputs:
    def __init__(self):
        self.events = []

    def set_events(self):
        self.events = pygame.event.get()

    def get_events(self): # a getter
        """Will return ALL the events"""
        return self.events

    def is_drawing(self):
        """used to figure out if the user is currently drawing"""
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True
    
    def is_exit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False

class graphics:
    def __init__(self, input_manager):
        self.input_manager = input_manager # needs input_manager to figure out position for drawing
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))
    
    def start_graphics(self):
        pygame.display.set_caption("EleArt")
            
class level_1:
    def __init__(self):
        # does not need input_manager, drawing will be done in the main() class
        pass

if __name__ == "__main__":
    main()