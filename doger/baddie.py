import pygame

class Baddie():

    def __init__(self):
        
        self.img_address = "/home/layback_thunder/Desktop/pract_code/Projects/pygame_pract/images/small_banana.bmp"
        self.player_image = pygame.image.load(self.img_address)