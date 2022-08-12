import pygame, random, sys
from pygame.locals import *

from settings import Settings
from font import Font
from player import Player
from baddie import Baddie

class DogerMain:

    
    def __init__(self):

        pygame.init()
        # This object will help us keep rack on constants
        self.settings = Settings()
        self.font = Font()
        self.player = Player()
        self.baddie = Baddie()
        # This object will help us keep the program from running too fast.
        self.main_clock = pygame.time.Clock() 
        # Screen obj being created
        self.screen_size = (self.settings.screen_width, self.settings.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        # Caption for window
        pygame.display.set_caption('Dodger')

        # Player highest score per game
        self.top_score = 0
        # Current score while in game
        self.score = 0

        # Bad guy container
        self.baddies = []
        # Baddie counter
        self.baddie_add_counter = 0

        # Movement indicators
        self.move_left = self.move_right = self.move_up = self.down = False

        # Cheats
        self.reverse_cheat = self.slow_cheat = False
        
        # Make mouse cursor invisible
        pygame.mouse.set_visible(False)
    
    def drawText(self, text, font, surface, x, y):

        textobj = font.render(text, 1, self.settings.TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def playerHasHitBaddie(playerRect, baddies):

        for b in baddies:
            if playerRect.colliderrect(b['rect']):
                return True
        return False

    def waitForPlayerToPressKey(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        self.terminate() # doesn't work
                    return

    def activateCheatsKeyDown(self, event):
        # Keyboard input to activate cheats
        if event.key == K_z:
            self.reverse_cheat = True
        if event.key == K_x:
            self.slow_cheat = True
        return event

    def stopCheatsKeyUp(self, event):
        # Input deactivates cheats in exchnage for all your points
        if event.key == K_z:
            self.reverse_cheat = False
            self.score = 0
        if event.key == K_x:
            self.slow_cheat = False
            self.score = 0
        return event

    def activateMovementKeyDown(self, event):
        if event == K_LEFT or event.key == K_a:
            


    def keyDownEvents(self, event):
            if event.type == KEYDOWN:
                self.activateCheatsKeyDown(event)
            return event

    def keyUpEvents(self, event):
            if event.type == KEYUP:
                # Flags cheat variables to false
                self.stopCheatsKeyUp(event)
                # Quit Game
                if event.key == K_ESCAPE:
                    self.terminate()
            return event

    def terminate(self):

        pygame.quit()
        sys.exit()



    def introToGame(self):

        self.screen.fill(self.settings.BG_COLOR)
        # Name of game
        self.drawText(
            'Doger', self.font.font, self.screen, 
            (self.settings.screen_width / 2), (self.settings.screen_height / 2)
            )
        # Player action 
        self.drawText(
            'Press a key to start.', self.font.font, self.screen,
            (self.settings.screen_width / 2) - 30, (self.settings.screen_height / 2) + 50
            )
        # Permit text to apear
        pygame.display.update()
        # Player needs to take action
        self.waitForPlayerToPressKey()

    def preGame(self):

        # Baddie counter
        self.baddie_add_counter = 0
        # Baddies are reset to an empty container
        self.baddies = []
        # Reset score to 0
        self.score = 0
        # Player location at the start of the game
        self.player.player_rect.topleft = (
            self.settings.screen_width / 2, self.settings.screen_height - 50
            )
        # Movement indicators
        self.move_left = self.move_right = self.move_up = self.down = False
        # Cheats
        self.reverse_cheat = self.slow_cheat = False
        #Music goes here
    
    def _checkKeyboardEvents(self):
        # verifies user input if KEYDOWN or KEYUP events
        # ***This is the only for loop dictating the flow of the data type: event
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                self.terminate()
            # Checks keyboard to set movemnt & cheat code variables to True
            self.keyDownEvents(event)
            # Checks keyboard to set movemnt & cheat code variables to False
            # Checks for ESC to quit game
            self.keyUpEvents(event)
        
    
    def runGame(self):
        # Before game loop
        self.introToGame()

        # Game set-up loop, reset variables
        while True:
            self.preGame()

            # Game loop
            while True: 
                # if player alive and game is running, player gains points
                self.score += 1 # Should it be a method!
                self._checkKeyboardEvents()
                
                self.screen.fill(self.settings.BG_COLOR)

                pygame.display.update()



if __name__ == '__main__':
    # Make a game instance, and run the game.
    d = DogerMain()
    d.runGame()