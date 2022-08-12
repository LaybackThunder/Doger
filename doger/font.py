import pygame

class Font():

    def __init__(self):
        pygame.init()
        # Passing None uses the default font. 
        # Passing 48 gives the font a size of 48 points.
        self.font = pygame.font.SysFont(None, 48)
