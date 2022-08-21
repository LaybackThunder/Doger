import pygame

class Baddie():

    def __init__(self):
        
        self.img_address = "/home/layback_thunder/Desktop/pract_code/Projects/pygame_pract/images/Banana Bread/banana-bread-baked-oatmeal-3.bmp"
        self.baddie_image = pygame.image.load(self.img_address)