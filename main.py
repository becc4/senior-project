# imports
import pygame
from PIL import Image

# constants
# screen is talked display_surface in examples
screen_X = 1280
screen_Y = 720
    # height and width

# the locations of text
middle_X = screen_X // 2
middle_Y = screen_Y // 5

draw_X = (screen_X / 7)
draw_Y = (screen_Y / 7) * 6

change_X = (screen_X / 5) * 4
change_Y = (screen_Y / 7) * 6

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# graphics
prompt_SPACE = "graphics/blue.png"
prompt_ENTER = "graphics/red.png"
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
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))
        #pygame.display.flip()
    
    
    def game_loop(self):
        self.start()

        while self.running:
            curr_level = self.levels[0]
            # event loop
            for event in pygame.event.get():
                # check if game is ending
                if event.type == pygame.QUIT:
                    self.running = False                

                # check if the game is in the input, drawing state, and allows to draw
                if self.state_manager.get_state() == states[INPUT]:
                    # check if drawing in game
                    self.graphic_manager.drawing_prompt()
                    # grab the information from user_drawing and put it into the level
                    drawing, x, y = self.drawing_manager.user_drawing(event)

                    curr_level.update_drawing(drawing, x, y)

            # change states (as needed)
            if self.state_manager.manually_change_state():
                self.graphic_manager.clear_state_prompt(self.state_manager.get_state())

                # graphics: call and add graphics
                self.graphic_manager.change_state_prompt(self.state_manager.get_state())

                # if the level is over, move onto next level
                if self.state_manager.state == PROMPTING:
                    self.levels.pop(0)
            
            pygame.display.flip()
            for i in self.drawing_manager.curr_lines:
                print(i.first_loc, i.last_loc)

            print(self.levels)
        
        pygame.quit()
class level_1:
    """
    drawing straight lines over and over
    """
    def __init__(self):
        self.drawn_straight_lines_manager = drawn_straight_lines
        self.curr_lines = []
        self.previously_drawing = 0
        pass
    def update_drawing(self, drawing, x, y):
        """
        takes and processes the drawings, this one will record lines
        """
        # check if it is the first instance of the drawing
        if self.previously_drawing == False and drawing == True:
            self.curr_lines.append(self.drawn_straight_lines_manager([x, y]))
        if self.previously_drawing == True and drawing == False:
            self.curr_lines[-1].set_last([x, y])

        self.previously_drawing = drawing

        for i in self.curr_lines:
            print(i.first_loc, i.last_loc)

    def analysis(self):
        pass

class drawn_straight_lines:
    """
    Drawings, contains the surfaces for each part of the drawing
        Used in level_1
    """
    def __init__(self, first_loc):
        self.first_loc = first_loc #coordinates of the first object

        self.last_loc = [] #coordinates of the last object

    def set_last(self, last_loc):
        self.last_loc = last_loc
        

class graphics:
    def __init__(self):
        self.drawing_color = WHITE
        self.screen_color = BLACK
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))

        self.font = 'freesansbold.ttf'
        self.PROMPT_size = 32

        self.DRAW_size = 20

        # draw the screen
        self.screen.fill(self.screen_color)
        pygame.display.set_caption("EleArt")

    def get_screen(self):
        return self.screen
    
    def get_drawing_color(self):
        return self.drawing_color

    def draw_screen(self):
        self.screen.fill(self.screen_color)
        pygame.display.set_caption("EleArt")
    
    def clear_state_prompt(self, state):
        """clear the prompt from the screen"""
        # get size of png first
        img = 0
        if state == INPUT:
            img = Image.open(prompt_SPACE)
        else:
            img = Image.open(prompt_ENTER)
        
        x, y = img.size

        rect = pygame.Rect(change_X, change_Y, x, y)
        pygame.draw.rect(self.screen, self.screen_color, rect)
        #pygame.display.flip(rect)

    def add_to_screen(self, surface, loc):
        self.screen.blit(surface, loc)

    def change_state_prompt(self, state):
    # check if the game is in the first, prompting state
        if state == states[PROMPTING] or state == states[CONCLUSION]:
            print("prompt_ENTER")
            surface = pygame.image.load(prompt_ENTER)
            self.add_to_screen(surface, (change_X, change_Y))
        else:
            print("prompt_SPACE")
            surface = pygame.image.load(prompt_SPACE)
            self.add_to_screen(surface, (change_X, change_Y))
            
    def drawing_prompt(self):
        font = pygame.font.Font(self.font, self.DRAW_size)
        text = font.render("Drawing ON", True, self.drawing_color, self.screen_color)
        textRect = text.get_rect()

        # text for the prompt will always be displayed at 
        textRect.center = (draw_X, draw_Y)
        self.screen.blit(text, textRect)

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
            # user is ACTIVELY drawing
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
    
    def change_state_protical(self):
        # change all states
        if self.state == states[PROMPTING]:
            self.state = states[INPUT]
        elif self.state == states[INPUT]:
            self.state = states[CONCLUSION]
        elif self.state == states[CONCLUSION]:
            self.state = states[PROMPTING]

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
            return True
        
        if keys_pressed[pygame.K_RETURN]:
            # return the drawing state to start analysis
            #   only way to start analysis, will not time out
            if self.state == states[INPUT] or self.state == states[CONCLUSION]:
                if self.enter_down == False:
                # makes sure that it isn't just continuously changing states
                    self.change_state_protical()
                    self.enter_down = True
                    return True
        else:
            self.enter_down = False        
        
        return False

main()