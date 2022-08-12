import pygame

class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 600
        self.screen_height = 600
        # Color settings
        self.BG_COLOR = (53, 101, 77)
        self.TEXTCOLOR = (0, 0, 0)
        # How fast a computer will let the game go
        self.FPS = 60
        self.BADDIEMINSIZE = 10
        self.BADDIEMAXSIZE = 40
        self.BADDIEMINSPEED = 1
        self.BADDIEMAXSPEED = 8
        self.ADDNEWBADDIERATE = 6
        # Set up player speed
        self.PLAYERMOVERATE = 5