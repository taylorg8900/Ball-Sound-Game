# Taylor Gebhard
# CS1400 - MWF 11:30

# this is pretty much here for me learn how to use masks and surfaces
# doesnt matter or have any functionality

import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CLOCK_DELAY = 30
TITLE = ''

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()


    surface = pygame.Surface((100,100))
    pygame.draw.circle(surface, (255,255,255), (50,50), 40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(surface, (50,50))
        pygame.display.flip()
        clock.tick(CLOCK_DELAY)

main()