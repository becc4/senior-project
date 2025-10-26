# the original main was poorly organized

# imports
import pygame
from PIL import Image

# constants
# screen is talked display_surface in examples
screen_X = 1280
screen_Y = 720

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

"""
STATES
prompting - sets up the prompt of the exercise
    Will include the start animation for the puzzle
input - where the user can actually draw
conclusion - completes the exercise
    Will include the end animation for the puzzle as well as analysis
"""
PROMPTING = 0   # Can be changed with ENTER
INPUT = 1       # input can be changed with SPACE
CONCLUSION = 2  # Can be changed with ENTER
states = ["PROMPTING", "INPUT", "CONCLUSION"]

class main:
    def __init__(self):
        # instances of other classes
        self.state_manager = change_state()
        self.graphic_manager = graphics()
        self.drawing_manager = drawing()

        self.levels = [level_1()]

        # make the game run
        self.running = True
        self.game_loop()


    def start(self):
        """
        initalizing pygame and the display
        """
        pygame.init()
        
    
    def game_loop(self):
        self.graphic_manager.start_graphics()

        cycles = 0 # cycles is short for game cycles

        # while game is running
        while self.running:
            cycles += 1
            #print(cycles)
            # make sure the game is still running:
            if len(self.levels) <= 0:
                self.running = False
            
            for event in pygame.event.get():
                # check if game was manually ended
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            # initializes the screen at the beginning of every game loop
            # clears screen
            self.graphic_manager.clear_screen()

            # get old state
            old_state = self.state_manager.get_state()

            # check to see if state has changed
            self.state_manager.check_change_state()

            # get new state
            state = self.state_manager.get_state()
            print(state)

            # check to see if should pop
            if state == states[PROMPTING] and old_state == states[CONCLUSION]:
                self.levels.pop(0)

            if len(self.levels) <= 0:
                # check if game has run out
                break

            cur_level = self.levels[-1]

            if state == states[PROMPTING]:
                cur_level.PROMPTING()
            elif state == states[INPUT]:
                cur_level.INPUT()
            elif state == states[CONCLUSION]:
                cur_level.CONCLUSION()
            else:
                # troubleshooting
                print("state UNKNOWN")

            # give state prompts
            self.graphic_manager.change_state_prompt(state)

            pygame.display.update()

class graphics():
    def __init__(self):
        self.drawing_color = WHITE
        self.screen_color = BLACK
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))

        self.font = 'freesansbold.ttf'
        self.PROMPT_size = 32

        self.DRAW_size = 20

        # locations for drawing prompt
        self.draw_X = (screen_X / 7)
        self.draw_Y = (screen_Y / 7) * 6

        # locations for prompt
        self.prompt_X = screen_X // 2
        self.prompt_Y = screen_Y // 5

        # prompts for phase change
        self.state_X = (screen_X / 5) * 4
        self.state_Y = (screen_Y / 7) * 6

    def blit_surfaces(self, surface, loc_x, loc_y):
        # blits surfaces
        self.screen.blit(surface, (loc_x, loc_y))

    def start_graphics(self):
        pygame.init()
        self.screen.fill(self.screen_color)
        pygame.display.set_caption("EleArt")
    
    def clear_screen(self):
        self.screen.fill(self.screen_color)
    
    def get_screen(self):
        return self.screen
    
    def get_drawing_color(self):
        return self.drawing_color
    
    def drawing_prompt(self):
        font = pygame.font.Font(self.font, self.DRAW_size)
        text = font.render("Drawing ON", True, self.drawing_color, self.screen_color)
        textRect = text.get_rect()

        # text for the prompt will always be displayed at 
        textRect.center = (self.draw_X, self.draw_Y)
    
    def change_state_prompt(self, state):
        if state == states[PROMPTING]:
            surface = pygame.Surface((100,200))
            surface.fill('orange')

            self.blit_surfaces(surface, self.state_X, self.state_Y)
        elif state == state[INPUT]:
            surface = pygame.Surface((100,200))
            surface.fill('blue')

            self.blit_surfaces(surface, self.state_X, self.state_Y)
        else:
            surface = pygame.Surface((100,200))
            surface.fill('red')

            self.blit_surfaces(surface, self.state_X, self.state_Y)

class drawing(graphics):
    def __init__(self):
        super().__init__()
        self.drawing = False
        self.last_position = None
        self.curr_lines = []

    def user_drawing(self, event):
        """
        Checks if the user is drawing or not, and if so, will draw
        """
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # The user is drawing
            self.drawing = True
            self.last_position = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # The user is not drawing
            self.drawing = False
        if event.type == pygame.MOUSEMOTION and self.drawing == True:
            # user is ACTIVELY drawing, this is where the drawing is
            pygame.draw.line(self.screen, self.drawing_color, self.last_position, event.pos, 2)
            self.last_position = event.pos
        
        # return all the information for levels to be analyzed
        # returns if currently drawing and location of mouse
        return [self.drawing, x, y]

class change_state:
    def __init__(self):
        self.state = states[PROMPTING]
        self.enter_down = False
    
    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state

    def check_change_state(self):
        """
        main's entrance into change_state class, checks for manual and 
        time-out state changes
        """
        self.manually_change_state()
    
    def change_state_protical(self):
        # change all states
        if self.state == states[PROMPTING]:
            self.set_state(states[INPUT])
        elif self.state == states[INPUT]:
            self.set_state(states[CONCLUSION])
        elif self.state == states[CONCLUSION]:
            self.set_state(states[PROMPTING])

        print("STATE IS NOW ", self.state)

        # remove text
        
    def manually_change_state(self):
        """
        makes sure that enter isn't already being pushed. If enter isn't, then will proceed
        """
        # check to manually change state
        keys_pressed = pygame.key.get_pressed()
        
            # space bar only way to jump out of prompting states, should also time out
        if keys_pressed[pygame.K_SPACE] and self.state == states[PROMPTING]:
            self.change_state_protical()
            #return True
        
        if keys_pressed[pygame.K_RETURN]:
            # return the drawing state to start analysis
            #   only way to start analysis, will not time out
            if self.state == states[INPUT] or self.state == states[CONCLUSION]:
                if self.enter_down == False:
                # makes sure that it isn't just continuously changing states
                    self.change_state_protical()
                    self.enter_down = True
                    #return True
        else:
            self.enter_down = False        
        
        #return False
    
class level_0:
    """
    master parent class for all child classes
    """
    def __init__(self):
        self.graphics_manager = graphics()
        self.curr_lines = []
        self.previously_drawing = 0    
        self.prompt = 0 # this will have to be manually overwritten in all child classes
        self.scene = 0 # this will be the scene


    def send_prompt(self):
        """graphs the initial prompt and sends it to main, who takes it to graphics"""
        self.graphics_manager.blit_surfaces(self.prompt, screen_X/2, screen_Y / 12)

    def send_scene(self):
        """
        sends graphics of the scene, background
        """
        self.graphics_manager.blit_surfaces(self.scene, 0, 0)
    
    def send_drawing(self):
        """show drawings"""
        for i in self.curr_lines:
            self.graphics_manager

    def start_level(self):
        self.send_scene()
        self.send_prompt()
        self.send_drawing()
    
class level_1(level_0):
    """
    drawing straight lines over and over

    Follow left to right, along a line of a ladder
    """
    def __init__(self):
        super().__init__()
        self.prompt = pygame.Surface((screen_X//3 * 2, screen_Y/8))
        self.prompt.fill("green")

        self.scene = pygame.Surface((screen_X, screen_Y))
        self.scene.fill("yellow")
        
    
    def PROMPTING(self):
        """
        manages the prompting of level 1
            Gives the message to main, who takes it to graphics who displays it
            Manages any animation
        """
        # every level will have this
        self.start_level()
        #self.drawn_lines_manager.draw_all_points(self.graphics_manager)

    def INPUT(self):
        """
        manages the input of level 1
        """
        self.start_level()
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                curr_drawing = True
            self.update_drawing(curr_drawing, x, y)
        
        self.drawn_lines_manager.draw_all_points()

    def CONCLUSION(self):
        """
        manages the conclusion of level 1, including analysis
        """
        self.start_level()
        self.drawn_lines_manager.draw_all_points()

        
    def update_drawing(self, curr_drawing, x, y):
        """
        takes and processes the drawings, this one will record lines
        curr_drawing = whether or not it's currently drawing
        """
        # check if it is the first instance of the drawing
        if self.previously_drawing == False and curr_drawing == True:
            self.curr_lines.append(self.drawn_lines_manager([x, y]))
        
        # check if it is the last instance of the drawing
        if self.previously_drawing == True and curr_drawing == False:
            self.curr_lines[-1].set_last([x, y])

        self.previously_drawing = curr_drawing

        #for i in self.curr_lines:
        #    print(i.first_loc, i.last_loc)

    def analysis(self):
        pass

class drawn_lines:
    """
    Drawings, contains the surfaces for each part of the drawing
        Used in level_1
    """
    def __init__(self, first_loc):
        self.graphics_manager = graphics
        self.first_loc = first_loc #coordinates of the first object

        self.all_points = [] # coordinates of all the objects, a list of lists 

        self.last_loc = [] #coordinates of the last object

    def add_points(self, x, y):
        self.all_points.append([x, y])

    def set_last(self, last_loc):
        self.last_loc = last_loc

    def draw_all_points(self):
        for i in self.all_points:
            x = i[0]
            y = i[1]
            surface = pygame.Surface((1,1))
            surface.fill(self.graphics_manager.drawing_color)
            self.graphics_manager.blit_surfaces(surface, x, y)


main()