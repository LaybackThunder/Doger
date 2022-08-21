from turtle import speed
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
        # Baddie dimentions
        self.baddie_size = 0

        # Var to help id baddie code
        self.baddie_screen_pos_y = 0 - self.baddie_size

        # Player rect
        self.player_rect = self.player.player_rect

        # Movement indicators
        self.move_left = self.move_right = False
        self.move_up = False
        self.down = False

        # Cheats
        self.reverse_cheat = self.slow_cheat = False
        
        # Make mouse cursor invisible
        pygame.mouse.set_visible(False)

# -------------------------------------------------------
    def points(self):
        # if player alive and game is running, player gains points every cycle
        self.score += 1

    def terminate(self):
        pygame.quit()
        sys.exit()

    def waitForPlayerToPressKey(self):
        # Check if player wants to quit before starting game session
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        self.terminate() # doesn't work
                    return

# -------------------------------------------------------
    def keyDownActivateCheats(self, event):
        # Keyboard input to activate cheats
        if event.key == K_z:
            self.reverse_cheat = True
        if event.key == K_x:
            self.slow_cheat = True
        return event

    def keyUpStopCheats(self, event):
        # Input deactivates cheats in exchnage for all your points
        if event.key == K_z:
            self.reverse_cheat = False
            self.score = 0
        if event.key == K_x:
            self.slow_cheat = False
            self.score = 0
        return event

    def keyDownActivateMovement(self, event):
        # Flag player movement to True base on direction
        if event == K_LEFT or event.key == K_a:
            self.move_left = True
            self.move_right = False
            # Adds pixels to rect to move player to the left if within window
            if self.move_left and self.player.player_rect.left > 0:
                self.player.player_rect.move_ip(-1 * self.settings.PLAYERMOVERATE, 0)

        if event == K_RIGHT or event.key == K_d:
            self.move_left = False
            self.move_right = True
            # Adds pixels to rect to move player to the right if within window
            if self.move_right and self.player.player_rect.right < self.settings.screen_width:
                self.player.player_rect.move_ip(self.settings.PLAYERMOVERATE, 0)

        if event == K_UP or event.key == K_w:
            self.move_up = True
            self.move_down = False
            # Adds pixels to rect to move player to the up(top) if within window
            if self.move_up and self.player.player_rect.top > 0:
                self.player.player_rect.move_ip(0, -1 * self.settings.PLAYERMOVERATE)

        if event == K_DOWN or event.key == K_s:
            self.move_down = True
            self.move_up = False
            if self.move_down and self.player.player_rect.bottom < self.settings.screen_height:
                # Adds pixels to rect to move player to the down(bottom) if within window
                self.player.player_rect.move_ip(0, self.settings.PLAYERMOVERATE)

        return event
        
    def keyUpStopMovement(self, event):
        # Flag player movement to True base on direction
        if event.key == K_LEFT or event.key == K_a:
            self.move_left = False
        if event.key == K_RIGHT or event.key == K_d:
            self.move_right = False
        if event.key == K_UP or event.key == K_w:
            self.move_up = False
        if event.key == K_DOWN or event.key == K_s:
            self.move_down = False
        return event

    def keyDownEvents(self, event):
            if event.type == KEYDOWN:
                self.keyDownActivateMovement(event)
                self.keyDownActivateCheats(event)
            return event

    def keyUpEvents(self, event):
            if event.type == KEYUP:
                # Flags cheat variables to false
                self.keyUpStopMovement(event)
                self.keyUpStopCheats(event)
                # Quit Game
                if event.key == K_ESCAPE:
                    self.terminate()
            return event

    def setMoveingMouseEvent(self, event):
        if event.type == MOUSEMOTION:
            # If the mouse moves, move the player to the cursor.
            self.player.player_rect.centerx = event.pos[0]
            self.player.player_rect.centery = event.pos[1]
        return event

    def _getKeyboardEvents(self):
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
            # Checks for mouse movement.
            self.setMoveingMouseEvent(event)

# -------------------------------------------------------
    def addNewBaddies(self):

        # Empty baddie object
        new_baddie = {}

        if not self.reverse_cheat and not self.slow_cheat:
            self.baddie_add_counter += 1
        
        # If logic is true baddie is generated and appeneded into a list
        if self.baddie_add_counter == self.settings.ADDNEWBADDIERATE:
            # Reset counter to 0 to control baddie creation
            self.baddie_add_counter = 0
            # Baddie size is determine by random
            # Baddie size is rect size
            self.baddie_size = random.randint(
                self.settings.BADDIEMINSIZE, self.settings.BADDIEMAXSIZE
            ) 
            # New Baddie obj is created
            new_baddie = {
                'rect': pygame.Rect(random.randint(
                    0, self.settings.screen_width - self.baddie_size), self.baddie_screen_pos_y,
                    self.baddie_size, self.baddie_size # rect size is given
                    ),
                'speed': random.randint(
                    self.settings.BADDIEMINSPEED,
                    self.settings.BADDIEMAXSPEED
                    ),
                'surface': pygame.transform.scale(
                    self.baddie.baddie_image, (self.baddie_size, self.baddie_size)
                )
            }
            
            # Baddie obj is added into a list
            self.baddies.append(new_baddie)

    def baddieMovement(self):
        # Move baddie down
        for b in self.baddies:
            # Baddies move normal rates
            if not self.reverse_cheat and not self.slow_cheat:
                b['rect'].move_ip(0, b['speed'])
            # Baddies move up if condition is true
            elif self.reverse_cheat:
                b['rect'].move_ip(0, -5)
            # Baddies move slowly by one pixel per cycle
            elif self.slow_cheat:
                b['rect'].move_ip(0, 1)
             
    def removingBaddiesOffScreen(self):
        # delete baddies when off screen
        # self.baddies[:]: creates a copy
        for b in self.baddies[:]:
            if b['rect'].top > self.settings.screen_height:
                self.baddies.remove(b)

    def playerDidYouHitBaddie(self, playerRect, baddies):
        for b in baddies:
            if playerRect.colliderect(b['rect']):
                return True
        return False
    
# -------------------------------------------------------
    def _drawTheWorld(self):
        self.screen.fill(self.settings.BG_COLOR)
        self.drawScore()
        self.drawPlayerAndBaddies()
        pygame.display.update()

    def drawText(self, text, font, surface, x, y):
        textobj = font.render(text, 1, self.settings.TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def drawScore(self):
        # Draw the score and top score
        self.drawText('Score: %s' % (self.score), self.font.font, self.screen, 10, 0)
        self.drawText('Top Score: %s' % (self.top_score), self.font.font, self.screen, 10, 40)
    
    def drawPlayerAndBaddies(self):
        # Player is drawn
        self.screen.blit(self.player.player_image, self.player_rect)
        # Baddie is drawn
        for i in self.baddies[]:
            self.screen.blit(i['surface'], i['rect'])

# -------------------------------------------------------
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

    def preGameSetUp(self):

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

    def gameLoop(self):
        while True: 
            self._getKeyboardEvents()
            self.points()
            self.addNewBaddies()
            self.baddieMovement()
            self.removingBaddiesOffScreen()
            self._drawTheWorld()

            # Checks for player collition with baddie, if true game ends
            # And nested while loop breaks returning to the 1st while loop
            # top_score is updated if its score has a larger value
            if self.playerDidYouHitBaddie(self.player_rect, self.baddies):
                if self.score > self.top_score:
                    self.top_score = self.score
                break

            # Controls the speed of the computer
            self.main_clock.tick(60)

    def gameOver(self):
        # Stop the game and show the "Game Over" screen.
        # Stop music here
        # Play game over music here

        self.drawText('GAME OVER', self.font.font, self.screen, (
            self.settings.screen_width / 3), (self.settings.screen_height / 3)
            )
        self.drawText('Press a key to play again', self.font.font, self.screen, (
            self.settings.screen_width / 3) - 80, (self.settings.screen_height / 3) + 50
            )
        pygame.display.update()
        self.waitForPlayerToPressKey()
        # game over sound stops here
# -------------------------------------------------------

    def runGame(self):
        # Before game loop
        self.introToGame()

        # Game set-up loop, reset variables
        while True:
            # The game set-up, variables reset
            self.preGameSetUp()
            # The game logic plays out here
            self.gameLoop()
            # The game over logic runs
            self.gameOver()

        

if __name__ == '__main__':
    # Make a game instance, and run the game.
    d = DogerMain()
    d.runGame()

