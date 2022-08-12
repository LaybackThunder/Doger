import pygame

class Player():

    def __init__(self):
        
        self.img_address = "/home/layback_thunder/Desktop/pract_code/Projects/pygame_pract/images/Rustle.bmp"
        self.player_image = pygame.image.load(self.img_address)
        self.player_rect = self.player_image.get_rect()