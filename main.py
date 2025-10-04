# imports
import pygame

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

"""
STATES
prompting - sets up the prompt of the exercise
    Will include the start animation for the puzzle
input - where the user can actually draw
analyzing - when the program reads and analysizes the drawing
conclusion - completes the exercise
    Will include the end animation for the puzzle
"""
PROMPTING = 0
INPUT = 1
ANALYZING = 2
CONCLUSION = 3
states = ["PROMPTING", "INPUT", "ANALYZING", "CONCLUSION"]

class main:
    def __init__(self):
        # for drawing
        self.drawing = False
        self.last_position = None

        # instances of other classes
        self.state_manager = change_state()
        self.graphic_manager = graphics()

        # make the game run
        self.running = True
        self.game_loop()


    def start(self):
        """
        initalizing pygame and the display
        """
        pygame.init()
        self.graphic_manager.draw_screen()

    def user_drawing(self, event):
        """
        Checks if the user is drawing or not, and if so, will draw
        """
        self.running
        screen = self.graphic_manager.get_screen()
        drawing_color = self.graphic_manager.get_drawing_color()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # The user is drawing
            self.drawing = True
            self.last_position = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            # The user is not drawing
            self.drawing = False
            self.last_position = None

        if event.type == pygame.MOUSEMOTION and self.drawing == True:
            # user is ACTIVELY drawing
            pygame.draw.line(screen, drawing_color, self.last_position, event.pos, 2)
            self.last_position = event.pos
        
        pygame.display.flip()
    
    
    def game_loop(self):
        self.start()

        while self.running:
            # event loop
            for event in pygame.event.get():
                # check if game is ending
                if event.type == pygame.QUIT:
                    self.running = False                

            # check if the game is in the input, drawing state, and allows to draw
            if self.state_manager.get_state() == states[INPUT]:
                # check if drawing in game
                self.graphic_manager.drawing_prompt()
                self.user_drawing(event)

            # change states (as needed)
            if self.state_manager.manually_change_state():
                self.graphic_manager.clear_screen()
                
            # graphics: call and add graphics
            self.graphic_manager.change_state_prompt(self.state_manager.get_state())
            
        
        pygame.quit()

class graphics:
    def __init__(self):
        self.drawing_color = WHITE
        self.screen_color = BLACK
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))

        self.font = 'freesansbold.ttf'
        self.PROMPT_size = 32

        self.DRAW_size = 20
    
    def get_screen(self):
        return self.screen
    
    def get_drawing_color(self):
        return self.drawing_color

    def draw_screen(self):
        self.screen.fill(self.screen_color)
        pygame.display.set_caption("EleArt")

    def display_prompt(self, message):
        font = pygame.font.Font(self.font, self.PROMPT_size)
        text = font.render(message, True, self.drawing_color, self.screen_color)

        textRect = text.get_rect()

        # text for the prompt will always be displayed at 
        textRect.center = (change_X, change_Y)
        self.screen.blit(text, textRect)

        pygame.display.flip()
    
    def clear_screen(self):
        self.screen.fill(self.screen_color)

    def change_state_prompt(self, state):
    # check if the game is in the first, prompting state
        if state == states[PROMPTING]:
            message = "Press SPACE to skip"
            self.display_prompt(message)
        elif state == states[INPUT] or state == states[CONCLUSION]:
            message = "Press ENTER to continue"
            self.display_prompt(message)
    
    def drawing_prompt(self):
        font = pygame.font.Font(self.font, self.DRAW_size)
        text = font.render("Drawing ON", True, self.drawing_color, self.screen_color)
        textRect = text.get_rect()

        # text for the prompt will always be displayed at 
        textRect.center = (draw_X, draw_Y)
        self.screen.blit(text, textRect)

        pygame.display.flip()
        

class change_state:
    def __init__(self):
        self.state = states[PROMPTING]
    
    def get_state(self):
        return self.state
    
    def change_state_protical(self):
        # change all states
        if self.state == states[PROMPTING]:
            self.state = states[INPUT]
        elif self.state == states[INPUT]:
            self.state = states[ANALYZING]
        elif self.state == states[ANALYZING]:
            self.state = states[CONCLUSION]
        elif self.state == states[CONCLUSION]:
            self.state = states[PROMPTING]

        print("STATE IS NOW ", self.state)

        # remove text
        
    def manually_change_state(self):
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
                self.change_state_protical()
            return True
        
        # For TESTING, automatically change to state Conclusion
        if self.state == states[ANALYZING]:
            self.change_state_protical()
            return True
        
        return False

main()