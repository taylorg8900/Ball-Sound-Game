# Taylor Gebhard
# CS1400 - MWF 11:30

# FILE IS HERE BECAUSE I WANT TO KEEP A HISTORY FOR MY MAIN FILE
# made this right after i finally got all of the bouncing behavior working properly
# after learning trig for like 14 hours
# DO NOT CHANGE ANYTHING IN HERE

import pygame
import math

from ball import make_ball
from node import make_node, make_line

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CLOCK_DELAY = 120
TITLE = "bouncy ball music game"
GRAVITY = .1
IMMUNITY_FRAMES = 10


def main():
    pass
    # initial setup
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # setup media
    # images
    # noises
    noise_checker = pygame.mixer.Sound("sounds/excited5.ogg")

    # setup game data
    temp_node_list = []
    node_list = []
    line_list = []
    ball_list = []

    # main loop
    running = True
    node_amount = 0
    mouse_pressed = False

    while running:
        # fill the screen with black, so that old blits arent there anymore
        screen.fill((0, 0, 0))

        # exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        # if user clicks, place a ball
        if pygame.mouse.get_pressed()[0]:
            if not mouse_pressed:
                mouse = pygame.mouse.get_pos()
                ball = make_ball(mouse[0], mouse[1])
                ball_list.append(ball)
                mouse_pressed = True

        # else if user middle clicks, place a static ball spawner
        # else if user right clicks and is hovering over ball spawner, raise speed
        # else if user right clicks and is not hovering over ball spawner, place node

        elif pygame.mouse.get_pressed()[2]:
            if not mouse_pressed:
                mouse_pressed = True
                mouse = pygame.mouse.get_pos()
                node = make_node(mouse[0], mouse[1])
                node.draw_node()
                screen.blit(node.surface, [node.centerx, node.centery])
                node_amount += 1

                # add node to the node lists
                temp_node_list.append(node)
                node_list.append(node)

                if node_amount == 2:
                    # create line, and add to the line list
                    line_list.append(make_line(temp_node_list[0], temp_node_list[1]))
                    # reset node count and node list
                    node_amount = 0
                    temp_node_list = []

        # reset mouse_pressed at the end of the block
        else:
            mouse_pressed = False

        # logic for detecting if balls are hitting the lines
        for ball in ball_list:
            for line in line_list:
                if ball.immune == False:

                    # determine if masks are overlapping
                    offset_x = ball.centerx - line.left_node_x
                    offset_y = ball.centery - line.top_left_y

                    # after much learning trig again i am finally here (took a day and half, about 14-15 hours total?)

                    # ok so formula angle.reflected = 2(angle.line) - angle.incident_ray for calculating is what i need

                    # angle of incident_ray is the angle of the ball's vector as it moves
                    # it is calculated counterclockwise from the x axis
                    # think back to quadrants in trig

                    # quad 1
                    #   x and y velocities are both positive
                    #   angle here is arcsin(height/hypotenuse)
                    #   angles between values 0 - 90
                    #   taking cos(angle) will be positive
                    #   taking sin(angle) will be positive
                    # quad 2
                    #   y velocity is positive, x velocity is negative
                    #   angle here is 180 - arcsin(height/hypotenuse)
                    #   angles between values 90 - 180
                    #   taking cos(angle) will be negative
                    #   taking sin(angle) will be positive
                    # quad 3
                    #   x and y velocities are both negative
                    #   angle here is 180 - arcsin(height/hypotenuse) <- arcsin will be negative, since height is negative
                    #   angles between values 180 - 270
                    #   taking cos(angle) will be negative
                    #   taking sin(angle) will be negative)
                    # quad 4
                    #   y velocity is negative, x velocity is positive
                    #   angle here is 360 + arcsin(height/hypotenuse) <- arcsin will be negative, since height is negative
                    #   angles between values 270 - 360
                    #   taking cos(angle) will be positive
                    #   taking sin(angle) will be negative

                    # also need to calculate the angle of the line
                    # if line is 'left facing', or in quadrant 1, then angle of line = arcsin(height/hypotenuse)
                    # if line is 'right facing', or in quadrant 2, then angle of line = -1 * arcsin(height/hypotenuse)

                    # after finding the angle of reflection using the above formula and provided information
                    # we find the new x and y velocities for the ray/ball using:
                    # new x velocity: cos(angle) * speed
                    # new y velocity: sin(angle) * speed
                    # where speed is the hypotenuse of the ray/ball vector before hitting the line
                    speed = (ball.x_velocity ** 2 + ball.y_velocity ** 2) ** .5  # gives hypotenuse of ball's vector
                    quad_1 = ball.x_velocity > 0 and ball.y_velocity > 0
                    quad_2 = ball.x_velocity < 0 and ball.y_velocity > 0
                    quad_3 = ball.x_velocity < 0 and ball.y_velocity < 0
                    quad_4 = ball.x_velocity > 0 and ball.y_velocity < 0
                    ray_angle = 0
                    reflection_angle = 0

                    if quad_1:
                        ray_angle = math.degrees(math.asin(ball.y_velocity / speed))
                    elif quad_2:
                        ray_angle = 180 - math.degrees(math.asin(ball.y_velocity / speed))
                    elif quad_3:
                        ray_angle = 180 - math.degrees(math.asin(ball.y_velocity / speed))
                    elif quad_4:
                        ray_angle = 360 + math.degrees(math.asin(ball.y_velocity / speed))
                    # case for if ball has 0 x_velocity, like when it gets spawned in
                    else:
                        ray_angle = 270

                    if line.mask.overlap(ball.mask, (offset_x, offset_y)) and line.slant == "left facing":
                        line_angle = line.angle
                        reflection_angle = (2 * line_angle) - ray_angle
                        new_x_velocity = math.cos(math.radians(reflection_angle)) * speed
                        new_y_velocity = math.sin(math.radians(reflection_angle)) * speed

                        ball.x_velocity = new_x_velocity
                        ball.y_velocity = new_y_velocity
                    elif line.mask.overlap(ball.mask, (offset_x, offset_y)) and line.slant == "right facing":
                        line_angle = -1 * line.angle
                        reflection_angle = (2 * line_angle) - ray_angle
                        new_x_velocity = math.cos(math.radians(reflection_angle)) * speed
                        new_y_velocity = math.sin(math.radians(reflection_angle)) * speed

                        ball.x_velocity = new_x_velocity
                        ball.y_velocity = new_y_velocity

                # need to rethink how im calculating the angles and everything
                # if ball is moving right and line is slanted right
                # but with new way of calculating angle
                '''
                if ball.immune == False:
                    if line.mask.overlap(ball.mask, (offset_x,offset_y)) and line.slant == "left facing":
                        speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))

                        A = line.angle
                        normal = 90 - A # angle belonging to line purpendicular to the line
                        B = math.degrees(math.asin(abs(ball.y_velocity/speed)))

                        # if ball is approaching from the left of the normal line
                        if B < normal:
                            ball.x_velocity = math.cos(math.radians((2*A) + B)) * speed
                            ball.y_velocity = math.sin(math.radians((2*A) + B)) * speed

                        # if ball is approaching from the right of the normal line
                        elif B > normal:
                            ball.x_velocity = math.cos(math.radians((2 * A) - B)) * speed * -1
                            ball.y_velocity = math.sin(math.radians((2 * A) - B)) * speed * -1

                        else:
                            temp_x = ball.x_velocity
                            temp_y = ball.y_velocity
                            ball.x_velocity = temp_y
                            ball.y_velocity = temp_x

                    if line.mask.overlap(ball.mask, (offset_x,offset_y)) and line.slant == "right facing":
                        speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))
                        A = line.angle
                        normal = 90 - A  # angle belonging to line purpendicular to the line




                    elif line.mask.overlap(ball.mask, (offset_x,offset_y)) and line.slant == "right facing":
                        speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))

                        A = line.angle
                        normal = 90 - A
                    ball.immune = True
                '''

                # THE 2 COMMENTED IF STATEMENTS BELOW HERE WORK , OTHERS NOT SO MUCH
                # JUST KEEPING THEM AROUND IN CASE THEY ARE USEFUL
                # (PROBABLY NOT USEFUL SINCE THEY DON'T WORK)
                '''
                # if ball is moving right and line is slanted right
                if line.mask.overlap(ball.mask, (offset_x,offset_y)) and line.slant == "right facing" and ball.x_velocity >= 0:
                    speed = math.sqrt((ball.x_velocity**2) + (ball.y_velocity**2))
                    D = 90 - math.degrees(math.asin(ball.y_velocity / speed))
                    A = line.angle
                    B = 90 - A - D
                    C = (A - B)

                    # MATH.SIN USES RADIANS NOT ANGLES I COULD HAVE SAVED HOURS IF I KNEW THIS
                    ball.y_velocity = (math.sin(math.radians(C)) * speed)
                    ball.x_velocity = (math.cos(math.radians(C)) * speed) * -1

                # if ball is moving left and line is slanted left
                if line.mask.overlap(ball.mask, (offset_x, offset_y)) and line.slant == "left facing" and ball.x_velocity <= 0:
                    speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))
                    D = 90 - math.degrees(math.asin(ball.y_velocity / speed))
                    A = line.angle
                    B = 90 - A - D
                    C = (A - B)

                    ball.y_velocity = (math.sin(math.radians(C)) * speed)
                    ball.x_velocity =  (math.cos(math.radians(C)) * speed)
                '''

                '''
                # if ball is moving left and line is slanted right
                if line.mask.overlap(ball.mask, (offset_x,offset_y)) and line.slant == "right facing" and ball.x_velocity < 0:
                    speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))

                    # a little different since we don't technically need the angle of incidence (i think)
                    A = line.angle
                    C = math.degrees(math.asin(ball.y_velocity/speed))
                    B = A - C
                    ball.y_velocity = math.sin(math.radians(B + A)) * speed
                    ball.x_velocity = math.cos(math.radians(B + A)) * speed

                if line.mask.overlap(ball.mask, (offset_x,offset_y)) and line.slant == "left facing" and ball.x_velocity > 0:
                    speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))

                    # a little different since we don't technically need the angle of incidence (i think)
                    A = line.angle
                    C = math.degrees(math.acos(abs(ball.x_velocity)/speed))
                    B = A - C
                    ball.y_velocity = math.sin(math.radians(B + A)) * speed
                    ball.x_velocity =  math.cos(math.radians(B + A)) * speed


                if line.mask.overlap(ball.mask, (offset_x, offset_y)) and line.slant == "left facing" and ball.x_velocity > 0:
                    speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))
                    A = line.angle
                    C = math.degrees(math.acos(ball.x_velocity/speed))
                    B = A + C
                    D = 180 - B - C - A
                    ball.x_velocity = math.cos(math.degrees(D + C)) * speed * -1
                    ball.y_velocity = math.sin(math.degrees(D + C)) * speed * -1


                # if ball is moving right and line is slanted left
                if line.mask.overlap(ball.mask, (offset_x,offset_y)) and line.slant == "left facing" and ball.x_velocity > 0:
                    speed = math.sqrt((ball.x_velocity ** 2) + (ball.y_velocity ** 2))
                    A = line.angle
                    C = math.degrees(math.acos(ball.x_velocity / speed))
                    B = A - C
                    ball.y_velocity = math.sin(math.radians(B)) * speed * -1
                    ball.x_velocity = math.cos(math.radians(B)) * speed


                if line.mask.overlap(ball.mask, (offset_x, offset_y)) and line.slant == "right facing":
                    ball.y_velocity = ball.y_velocity * (-1 * y_bouncy) - GRAVITY
                    if ball.x_velocity_initialized == False:
                        ball.x_velocity = abs(ball.y_velocity )
                        ball.x_velocity_initialized = True
                    else:
                        ball.x_velocity *= x_bouncy + GRAVITY
                '''

                ###
                ##### THIS CODE IS THE ORIGINAL, VERY IMPORTANT AND SIGMA BASED 5HEAD MOMENT
                ###
                '''if line.mask.overlap(ball.mask, (offset_x,offset_y)):
                    ball.y_velocity = ball.y_velocity * -1 - GRAVITY
                    print("OH SHIT")'''
                ###
                #####
                ###

        # update display
        # blit balls to screen, and update their state
        for ball in ball_list:
            ball.move_ball(GRAVITY)
            ball.immune_frames += 1
            if ball.immune_frames == IMMUNITY_FRAMES:
                ball.immune = False
            screen.blit(ball.surface, [ball.centerx, ball.centery])

        # blit nodes
        for node in node_list:
            screen.blit(node.surface, [node.centerx, node.centery])

        # blit lines to screen
        for i in line_list:
            # i.draw_line()
            screen.blit(i.surface, [i.left_node_x, i.top_left_y])

        pygame.display.flip()
        clock.tick(CLOCK_DELAY)


def is_touching(object1, object2):
    if pygame.sprite.collide_mask(object1.mask, object2.mask):
        return True


main()