# imports
import pygame

# constants
screen_X = 1280
screen_Y = 720

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = 'Comic Sans MS'
class main:
    def __init__(self):
        pygame.init()

        # (only) instances of other classes
        self.input_manager = inputs()
        self.timer_manager = timer()
        self.graphic_manager = graphics(self.timer_manager)
        self.drawing_manager_user = drawing(self.input_manager, self.graphic_manager.screen)
        self.drawing_manager_teacher = drawing(self.input_manager, self.graphic_manager.screen)
        self.drawing_manager_teacher.drawing_color = BLACK

        # the levels of the game
        self.levels = [level_1(self.graphic_manager, self.drawing_manager_teacher), level_1(self.graphic_manager, self.drawing_manager_teacher)]
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

            """TIME OUT OF LEVEL"""
            if self.timer_manager.regular_gameloop_timer():
                self.levels.pop(0)
                self.drawing_manager_user.new_level()
                self.drawing_manager_teacher.new_level()

            """REGULAR GAMELOOP"""
            self.graphic_manager.regular_gameloop_graphics()
            # drawing user
            self.drawing_manager_user.check_if_drawing(self.input_manager.is_drawing())
            self.drawing_manager_user.blit_all_drawings()

            self.graphic_manager.update_display() # Goes LAST

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
    def __init__(self, timer_manager):
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))
        self.timer_manager = timer_manager
    
    def start_graphics(self):
        pygame.display.set_caption("EleArt")
        pygame.font.init()

    def blit_graphics(self, surface, loc_x, loc_y):
        self.screen.blit(surface, (loc_x, loc_y))
    
    def regular_gameloop_graphics(self):
        # user screen
        self.screen.fill(BLACK)

        # instructor screen
        instructor_screen = pygame.Surface((screen_X/4, screen_Y/4))
        instructor_screen.fill(WHITE)

        self.blit_graphics(instructor_screen, 0, 0)

        self.display_clock()

    def update_display(self):
        pygame.display.update()
    
    def display_clock(self):
        timer_font = pygame.font.SysFont(FONT, 50)

        time = self.timer_manager.get_time()

        total_seconds = time // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        timer_surface = timer_font.render(str(f"{minutes:02}:{seconds:02}"), False, WHITE)
        self.blit_graphics(timer_surface, screen_X/2 - timer_surface.get_width()/2, 0)

class drawing():
    def __init__(self, input_manager, screen):
        self.input_manager = input_manager
        self.events = self.input_manager.get_events()
        self.screen = screen

        self.drawing_color = WHITE

        self.was_just_drawing = False
        self.last_loc = ()

        self.lines = [] # all drawings

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
            self.lines.append([self.last_loc, new_loc])
        
        else:
            self.lines.append([new_loc, new_loc])
       
        self.last_loc = new_loc
        print("This is running")
    
    def blit_all_drawings(self):
        for i in self.lines:
            pygame.draw.line(self.screen, self.drawing_color, i[0], i[1], 2)

    def new_level(self):
        self.lines = []

class timer():
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        
        self.minutes = 10 #in minutes, for future customization
        self.milli_duration = self.minutes * 1000 #* 60 #duration in milliseconds
    
    def get_time(self):
        current_time = pygame.time.get_ticks()

        return self.milli_duration - (current_time - self.start_time)
    
    def regular_gameloop_timer(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.start_time >= self.milli_duration:
            self.start_time = current_time
            return True
        
        else:
            return False
    

class level_1:
    def __init__(self, graphic_manager, drawing_manager_teacher):
        # does not need input_manager, drawing will be done in the main() class
        self.graphic_manager = graphic_manager
        self.drawing_manager_teacher = drawing_manager_teacher

    def game(self):
        pass

if __name__ == "__main__":
    main()