# Taylor Gebhard
# CS1400 - MWF 11:30

import pygame
import math
import random

RADIUS = 10
WHITE = (255,255,255)
CYAN = (0,255,255)
RED = (255,0,0)

class Ball:

    GRAVITY = 1
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.radius = RADIUS
        self.centerx = self.x- RADIUS
        self.centery = self.y- RADIUS


        # using stuff from cs50ai, and https://www.pygame.org/docs/ref/surface.html
        # create a mask for detecting collision
        surface = pygame.Surface((round(RADIUS*2),round(RADIUS*2)))
        pygame.draw.circle(surface,(255,255,255),(RADIUS,RADIUS), RADIUS)
        self.mask = pygame.mask.from_surface(surface)

        # create the image of the ball
        transparent_surface = pygame.Surface((round(RADIUS*2),round(RADIUS*2)), pygame.SRCALPHA)
        transparent_surface.fill((0,0,0,0))
        pygame.draw.circle(transparent_surface,(255,255,255),(RADIUS,RADIUS), RADIUS)
        self.surface = transparent_surface

        # start making things for velocity
        # need acceleration(gravity), x_velocity, y_velocity
        # maybe have gravity in main, not in here
        self.x_velocity = 0
        self.y_velocity = 0

        # create immunity frames so that it stops tweaking out all the fucking time
        # prevents program from crashing if you place a ball right inside a line
        self.immune = True
        self.immune_frames = 0

    def move_ball(self, gravity):
        self.y_velocity -= gravity
        self.centery -= self.y_velocity
        self.centerx += self.x_velocity

class Spawner:

    def __init__(self, x_pos, y_pos, interval):

        self.centerx = x_pos
        self.centery = y_pos
        self.radius = RADIUS
        self.color = WHITE
        self.x = self.centerx - self.radius
        self.y = self.centery - self.radius
        self.interval = interval
        self.time = pygame.time.get_ticks()

        # create the same image as the ball, but hollow
        # don't need a mask


        transparent_surface = pygame.Surface((round(self.radius*2),round(self.radius*2)), pygame.SRCALPHA)
        transparent_surface.fill((0,0,0,0))
        pygame.draw.circle(transparent_surface,(self.color),(self.radius,self.radius),self.radius, (self.radius//5))
        self.surface = transparent_surface

    def interval_checker(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time >= self.interval:
            # have the self.time = current_time in here so it doesn't reset itself unless the condition is true
            # if you dont it doesnt work cuz it keeps resetting every frame in main while loop lol
            self.time = current_time
            return True
    def spawn_ball(self):
        ball = Ball(self.x,self.y)
        return ball

SIZE = 20
ABOVE_AMOUNT = 10 + (SIZE//2)
class Text:
    # class that will be used to give user feedback if they click on a spawner and increase/decrease speed
    # should be above spawner
    # have an update function within class that will make text go away each time it is called
        # change something like transparency, or coordinates, or size


    def __init__(self, x_pos, y_pos, mode):
        self.size = SIZE
        self.alphavalue = 255 # controls transparency of text


        if mode == "speed up":
            font = pygame.font.SysFont("arial",self.size)
            self.text = font.render("Speed up!",True,'white')
            self.text.set_alpha(self.alphavalue)
            text_rect = self.text.get_rect()
            text_rect.centerx = x_pos
            text_rect.centery = y_pos - ABOVE_AMOUNT
            self.text_rect = text_rect
        elif mode == "speed down":
            font = pygame.font.SysFont("arial", self.size)
            self.text = font.render("Speed down...", True, 'white')
            self.text.set_alpha(self.alphavalue)
            text_rect = self.text.get_rect()
            text_rect.centerx = x_pos
            text_rect.centery = y_pos - ABOVE_AMOUNT
            self.text_rect = text_rect

    def update_text(self):
        # need to modify the text, not its rect if i want the size to change
        # could change the rects coordinates to be fancy later, but that doesnt change size, only position
        # might just have a counter that if it gets too large will remove from list cuz idk how to do that stuff
        self.alphavalue -= 2
        self.text.set_alpha(self.alphavalue)

        self.text_rect.centery -= 1







def make_ball(x_pos, y_pos):
    ball = Ball(x_pos, y_pos)
    return ball
def make_spawner(x_pos, y_pos, interval):
    spawner = Spawner(x_pos,y_pos, interval)
    return spawner
def make_speed_text(x_pos, y_pos, mode="speed up"):
    text = Text(x_pos, y_pos, mode)
    return text


