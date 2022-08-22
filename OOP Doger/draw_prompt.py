import pyghelpers, pygame, sys

pygame.init()

screen_size = (600, 600)
screen = pygame.display.set_mode(screen_size)

while True: # game loop

    for event in pygame.event.get(): # checks for events
        if event.type == pygame.QUIT: # quit screen condition
            pyghelpers.textAnswerDialog(screen, (75, 80, 500, 150), 'Game is about to quit', 'Ok', 'None')
            sys.exit()
            
    pygame.display.flip() # draws elements per cycle

