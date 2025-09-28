# imports
import pygame

# constants
# screen is talked display_surface in examples
screen_X = 1280
screen_Y = 720
    # height and width

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Text
FONT = 'freesansbold.ttf'
FONT_SIZE = 32

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
states = [PROMPTING, INPUT, ANALYZING, CONCLUSION]

class main:
    def __init__(self):
        # for drawing
        self.drawing = False
        self.drawing_color = WHITE
        self.last_position = None
        self.state = states[PROMPTING]

        # cosmetic
        self.screen_color = BLACK

        # make the game run
        self.running = True
        main.game_loop(self)


    def start(self):
        """
        initalizing pygame and the display
        """
        pygame.init()
        self.screen = pygame.display.set_mode(size=(screen_X, screen_Y))
        self.screen.fill(self.screen_color)
        pygame.display.set_caption("EleArt")

    def user_drawing(self, event):
        """
        Checks if the user is drawing or not, and if so, will draw
        """
        self.running

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
            pygame.draw.line(self.screen, self.drawing_color, self.last_position, event.pos, 2)
            self.last_position = event.pos
        
        pygame.display.flip()
        
    def display_prompt(self, message):
        font = pygame.font.Font(FONT, FONT_SIZE)
        text = font.render(message, True, self.drawing_color, self.screen_color)

        textRect = text.get_rect()

        # text for the prompt will always be displayed at 
        textRect.center = (screen_X // 2, screen_Y // 5)
        self.screen.blit(text, textRect)
    
    def game_loop(self):
        main.start(self)

        while self.running:
            # event loop
            for event in pygame.event.get():
                # check if game is ending
                if event.type == pygame.QUIT:
                    self.running = False

                # check to manually change state
                keys_pressed = pygame.key.get_pressed()
                
                    # space bar only way to jump out of the animation states
                if keys_pressed[pygame.K_SPACE]:
                    if self.state == states[PROMPTING]:
                        self.state = states[INPUT]
                        print("STATE IS NOW ", self.state)
                    elif self.state == states[CONCLUSION]:
                        self.state = states[PROMPTING]
                        print("STATE IS NOW ", self.state)
                
                # return the drawing state to start analysis
                #   only way to start analysis, will not time out
                if keys_pressed[pygame.K_RETURN] and self.state == states[INPUT]:
                    self.state = states[ANALYZING]
                    print("STATE IS NOW ", self.state)
                
                # For TESTING
                if self.state == states[ANALYZING]:
                    self.state = states[CONCLUSION]
                    print("STATE IS NOW ", self.state)
                
            
            # check if the game is in the first, prompting state
            if self.state == states[PROMPTING]:
                message = "This Works"
                main.display_prompt(self, message)

            # check if the game is in the input, drawing state
            elif self.state == states[INPUT]:
                # check if drawing in game
                main.user_drawing(self, event)
                
            # draw in the game, cosmetic

            
        
        pygame.quit()

main()