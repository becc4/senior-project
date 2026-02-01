# imports
import pygame

# constants
screen_X = 1280
screen_Y = 720

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
class main:
    def __init__(self):
        pygame.init()

        # (only) instances of other classes
        self.input_manager = inputs()
        self.graphic_manager = graphics()
        self.drawing_manager = drawing(self.input_manager, self.graphic_manager.screen)

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

            self.drawing_manager.check_if_drawing(self.input_manager.is_drawing())

            """EXIT CLAUSES"""
            # exit if there are no more levels
            if len(self.levels) <= 0:
                self.running = False
            
            # exit if the game manually ended
            if self.input_manager.is_exit():
                self.running = False

            self.graphic_manager.update_display()        

"""
has no parameters, only returns. 
"""
class inputs:
    def __init__(self):
        self.events = []
        self.event = 0

    def set_events(self):
        self.events = pygame.event.get()

    def get_events(self): # a getter
        """Will return ALL the events"""
        return self.events

    def is_drawing(self):
        """used to figure out if the user is currently drawing"""
        return pygame.mouse.get_pressed()[0]
    
    def is_exit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False

class graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))
    
    def start_graphics(self):
        pygame.display.set_caption("EleArt")

    def blit_graphics(self, surface, loc_x, loc_y):
        self.screen.blit(surface, (loc_x, loc_y))

    def update_display(self):
        pygame.display.update()

class drawing():
    def __init__(self, input_manager, screen):
        self.input_manager = input_manager
        self.events = self.input_manager.get_events()
        self.screen = screen

        self.drawing_color = WHITE

        self.was_just_drawing = False
        self.last_loc = ()

    def update_events(self):
        self.events = self.input_manager.get_events()

    def check_if_drawing(self, is_drawing):
        if is_drawing == True:
            self.user_drawing()
            self.was_just_drawing = True
        else:
            self.was_just_drawing = False

    def user_drawing(self):
        """Only called when was_just_drawing == True"""
        new_loc = pygame.mouse.get_pos()

        if self.was_just_drawing == True:
            pygame.draw.line(self.screen, self.drawing_color, self.last_loc, new_loc, 2)
        
        else:
            pygame.draw.circle(self.screen, self.drawing_color, new_loc, 2)
       
        self.last_loc = new_loc
        print("This is running")

class level_1:
    def __init__(self):
        # does not need input_manager, drawing will be done in the main() class
        pass

if __name__ == "__main__":
    main()