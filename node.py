# Taylor Gebhard
# CS1400 - MWF 11:30
import pygame
import math
RADIUS = 11
cyan = (0,255,255)

class Node:
    #RADIUS = 15
    HEIGHT = (RADIUS * 2)//3
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.centerx = self.x - RADIUS
        self.centery = self.y - RADIUS

        # using stuff from cs50ai, and https://www.pygame.org/docs/ref/surface.html
        # don't need a mask for collision
        # create the image of the node
        transparent_surface = pygame.Surface((round(RADIUS * 2), round(RADIUS * 2)), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(transparent_surface, (0, 255, 255), (RADIUS, RADIUS), RADIUS)
        self.surface = transparent_surface

class Line:
    def __init__(self, x1, y1, x2, y2):
        LINE_WIDTH = 3

        x1 = x1 + RADIUS
        x2 = x2 + RADIUS
        y1 = y1 + RADIUS
        y2 = y2 + RADIUS
        # define where the node on the left is, and where node on the right is
        # node on left has smaller x value
        # node on right has larger x value
        if x1 < x2:
            self.left_node_x = x1
            self.left_node_y = y1
            self.right_node_x = x2
            self.right_node_y = y2

        else:
            self.left_node_x = x2
            self.left_node_y = y2
            self.right_node_x = x1
            self.right_node_y = y1

        # define width, height, and top left position for blitting in main
        # top left will be left node x, and top left corner y
        self.width = self.right_node_x - self.left_node_x
        if self.left_node_y < self.right_node_y:
            self.height = self.right_node_y - self.left_node_y
            self.top_left_y = self.left_node_y
        else:
            self.height = self.left_node_y - self.right_node_y
            self.top_left_y = self.right_node_y
        # define the length of the line
        self.length = (self.height**2 + self.width**2) **.5

        ### draw a line from the left node to the right node
        ### size of surface is equal to width and height
        ### need to have a mask, and a surface

        # make surface and mask to be displayed with blit
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        transparent_surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        if self.left_node_y < self.right_node_y: # if line goes from top left to bottom right
            pygame.draw.line(transparent_surface, (cyan),(0,0),(self.width,self.height),LINE_WIDTH)
            pygame.draw.line(surface, (cyan),(0,0),(self.width,self.height),LINE_WIDTH)

        else: # if line goes from bottom left to top right
            pygame.draw.line(transparent_surface, (cyan), (0, self.height), (self.width, 0), LINE_WIDTH)
            pygame.draw.line(surface, (cyan), (0, self.height), (self.width, 0), LINE_WIDTH)

        self.surface = transparent_surface
        self.mask = pygame.mask.from_surface(surface)

        # find the angle of the line, to determine how to multiply the ball's x and y velocity
        # i think i only need to use sin() for this? since opposite/adjacent and using tan() would be one more step
        #angle_radians = math.atan(self.height/self.width)
        #angle_degrees = math.degrees(angle_radians)
        #self.angle = angle_degrees
        #self.angle = math.degrees(math.atan(self.height/self.width))
        self.angle = math.degrees(math.asin(self.height/self.length))
        # find out if line is slanted to the right, or to the left
        if self.left_node_y < self.right_node_y:
            self.slant = "right facing"
        else:
            self.slant = "left facing"


def make_node(x_pos,y_pos):
    node = Node(x_pos,y_pos)
    return node

def make_line(node1, node2):
    line = Line(node1.centerx, node1.centery, node2.centerx, node2.centery)
    return line
