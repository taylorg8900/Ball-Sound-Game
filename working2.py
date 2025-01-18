# Taylor Gebhard
# CS1400 - MWF 11:30

# THIS FILE IS HERE AFTER I GOT BALL SPAWNERS WORKING
# ALSO HAVING THE ABILITY TO INCREASE OR DECREASE THEIR SPEED IS WORKING NOW

import pygame
import math

from pygame import KSCAN_A

from ball import make_ball, make_spawner
from node import make_node, make_line

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CLOCK_DELAY = 120
TITLE = "bouncy ball music game"
GRAVITY = .1
IMMUNITY_FRAMES = 1
# not sure how this is measured tbh so imma set it to clock delay so its maybe once a second
# pretty sure it is actually measured in milliseconds
SPAWNER_TICKS = 1000  # not sure how this is measured tbh so imma set it to clock delay so its maybe once a second


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
    spawner_list = []
    counter = 0

    # i guess we doing custom events now (or at least trying to, idk how they work really)
    # people say you need to write it this way with the +1 at the end idk why tho

    SPAWN_BALL = pygame.USEREVENT + 1
    # pygame.time.set_timer(SPAWN_BALL, 10000)

    # main loop
    running = True
    node_amount = 0

    while running:
        # fill the screen with black, so that old blits arent there anymore
        screen.fill((0, 0, 0))
        # timer = pygame.time.set_timer(millis=100)

        # controls
        # left click or 1 = place ball
        # middle click or 3 = place spawner
        # right click or 2 = place node
        # left click on spawner = raise speed
        # right click on spawner = lower speed
        #   if speed is less than 0 delete spawner

        mouse = pygame.mouse.get_pos()
        left_click = False
        right_click = False
        middle_click = False
        key_1 = False
        key_2 = False
        key_3 = False
        key_4 = False
        key_5 = False

        # exit condition
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False

            # have moussebuttondown and keydown in seperate conditionals
            # the reason for this is because you cant perform event.key on mousebuttondown
            # also calling pygame.mouse.get_pressed() in event.type == pygame.keydown wont work
            elif event.type == pygame.MOUSEBUTTONDOWN:

                left_click = pygame.mouse.get_pressed()[0]
                right_click = pygame.mouse.get_pressed()[2]
                middle_click = pygame.mouse.get_pressed()[1]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                key_1 = event.key == pygame.K_1
                key_2 = event.key == pygame.K_2
                key_3 = event.key == pygame.K_3
                key_4 = event.key == pygame.K_4
                key_5 = event.key == pygame.K_5

        # controls from keyboard or mouse input, gathered with for event loop above
        if left_click or key_1:
            ball = make_ball(mouse[0], mouse[1])
            ball_list.append(ball)
        elif right_click or key_2:
            node = make_node(mouse[0], mouse[1])
            # add node to the node lists
            temp_node_list.append(node)
            node_list.append(node)
            node_amount += 1
            if node_amount == 2:
                # create line, and add to the line list
                line_list.append(make_line(temp_node_list[0], temp_node_list[1]))
                # reset node count and node list
                node_amount = 0
                temp_node_list = []
        elif middle_click or key_3:
            spawner = make_spawner(mouse[0], mouse[1], SPAWNER_TICKS)
            spawner_list.append(spawner)

        # logic for ball spawners
        for spawner in spawner_list:
            # need to get mouse coords outside of event loop since the events wont pick it up if it isnt moving

            # check if mouse x coord and mouse y coord is touching the spawner
            # this is pretty poorly designed and i should fix it later cuz its not reusable at all
            mouse_x_touching = mouse[0] >= spawner.x and mouse[0] <= spawner.x + 2 * spawner.radius
            mouse_y_touching = mouse[1] >= spawner.y and mouse[1] <= spawner.y + 2 * spawner.radius
            mouse_touching = mouse_x_touching and mouse_y_touching
            print(mouse_x_touching)
            # if left click on spawner, speed it up AKA decrease SPAWNER_TICKS by idk like 100 ms or something
            # if right click on spawner, slow it down AKA increase SPAWNER_TICKS by 100
            # if SPAWNER_TICKS gets over 10 seconds how about we get rid of it
            # dont let interval get below  0

            # faster
            if mouse_touching and key_4:
                spawner.interval -= 100
                if spawner.interval < 100:
                    spawner.interval = 100
                else:
                    # text
                    pass


            # slower
            elif mouse_touching and key_5:
                spawner.interval += 100
                if spawner.interval > 2000:
                    spawner.interval = 2000
                else:
                    # text
                    pass

            # call interval checker function
            # if true, spawn a ball at the spawners location
            if spawner.interval_checker():
                ball = make_ball(spawner.centerx, spawner.centery)
                ball_list.append(ball)

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
                        ball.centerx += ball.x_velocity
                        ball.centery -= ball.y_velocity

                    elif line.mask.overlap(ball.mask, (offset_x, offset_y)) and line.slant == "right facing":
                        line_angle = -1 * line.angle
                        reflection_angle = (2 * line_angle) - ray_angle
                        new_x_velocity = math.cos(math.radians(reflection_angle)) * speed
                        new_y_velocity = math.sin(math.radians(reflection_angle)) * speed

                        ball.x_velocity = new_x_velocity
                        ball.y_velocity = new_y_velocity
                        ball.centerx += ball.x_velocity
                        ball.centery -= ball.y_velocity

        # update display

        # update ball state, remove from list if not in bounds, and blit to screen
        for ball in ball_list:
            # update balls
            ball.move_ball(GRAVITY)
            ball.immune_frames += 1
            if ball.immune_frames >= IMMUNITY_FRAMES:
                ball.immune = False
            # if ball is off screen remove it
            x_position = ball.centerx - ball.radius
            y_position = ball.centery - ball.radius
            if x_position > SCREEN_WIDTH or y_position > SCREEN_HEIGHT:
                ball_list.remove(ball)
            # blit to screen
            screen.blit(ball.surface, [ball.centerx, ball.centery])
        print(ball_list)

        # blit nodes
        for node in node_list:
            screen.blit(node.surface, [node.centerx, node.centery])

        # blit lines
        for i in line_list:
            # i.draw_line()
            screen.blit(i.surface, [i.left_node_x, i.top_left_y])

        # blit spawners
        for spawner in spawner_list:
            screen.blit(spawner.surface, [spawner.x, spawner.y])

        # blit text
        font = pygame.font.SysFont("timesnewroman", 20)
        text = font.render("esc to quit\n1 = ball\n2 = node\n3 = spawner\n4 = slowdown\n5 = speedup", True, "white")
        text_rect = text.get_rect()
        screen.blit(text, [0, 0])

        pygame.display.flip()
        clock.tick(CLOCK_DELAY)


def is_touching(object1, object2):
    if pygame.sprite.collide_mask(object1.mask, object2.mask):
        return True


main()