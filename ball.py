from config import *
from math import *
from random import *
from log import Log
import pygame
import math
import random
import collision as col
from datetime import datetime

pygame.init()

random.seed(datetime.now())

class Ball():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = BALL_SIZE
        self.color = WHITE
        self.rect = (self.x, self.y, self.size, self.size)

        self.reset()
        
    def reset(self):
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2

        angle = uniform(pi/4, -pi/4)

        self.xspeed = 0.2 * cos(angle)
        self.yspeed = 0.2 * sin(angle)

        if randrange(0, 1) < 0.5:
            self.xspeed *= -1

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def get_pos(self):
        return [self.x, self.y]

    def try_update(self, dt):
        x = self.x + self.xspeed * dt
        y = self.y + self.yspeed * dt

        return x, y

    def update(self, dt):
        self.x += self.xspeed * dt
        self.y += self.yspeed * dt
    
        self.rect = (self.x, self.y, self.size, self.size)

    def check_paddle_left(self, paddle_x, paddle_y, nx, ny):
        paddle_height = PADDLE_SIZE[1]
        paddle_width = PADDLE_SIZE[0]

        collision_point = col.get_segment_intersection(self.x, self.y, nx, ny, paddle_x + paddle_width, paddle_y, paddle_x + paddle_width, paddle_y + paddle_height)
        if collision_point is not None:
            # https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
            print("collided with left paddle")

            # take diff from middle of paddle
            relative_intersection = (paddle_y + (paddle_height / 2)) - collision_point[1]
            normalized = relative_intersection / (paddle_height/2)

            angle = normalized * col.BOUNCE_ANGLE # multiply by acceleration here
    
            self.xspeed = 0.2 * cos(angle)
            self.yspeed = 0.2 * -sin(angle)

            self.x = paddle_x + paddle_width

            return True

        return False


    def check_paddle_right(self, paddle_x, paddle_y, nx, ny):
        paddle_height = PADDLE_SIZE[1]
        paddle_width = PADDLE_SIZE[0]

        collision_point = col.get_segment_intersection(self.x + BALL_SIZE, self.y, nx + BALL_SIZE, ny, paddle_x, paddle_y, paddle_x, paddle_y + paddle_height)
        if collision_point is not None:
            # https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
            print("collided with right paddle")

            # take diff from middle of paddle
            relative_intersection = (paddle_y + (paddle_height / 2)) - collision_point[1]
            normalized = relative_intersection / (paddle_height/2)

            angle = normalized * col.BOUNCE_ANGLE # multiply by acceleration here

            self.xspeed = 0.2 * -cos(angle)
            self.yspeed = 0.2 * -sin(angle)

            self.x = paddle_x - BALL_SIZE - paddle_width

            return True

        return False

    def edges(self, nx, ny):
        left_score = 0
        right_score = 0

        top1 = col.LEFT_WINDOW_TOP
        top2 = col.RIGHT_WINDOW_TOP

        bottom1 = col.LEFT_WINDOW_BOTTOM
        bottom2 = col.RIGHT_WINDOW_BOTTOM

        # check if ball intersects at the top edge
        collision_point = col.get_segment_intersection(self.x, self.y, nx, ny, top1[0], top1[1], top2[0], top2[1])
        if collision_point is not None:
            print("top edge")
            self.yspeed *= -1
            self.y = collision_point[1]+1

            return [0, 0]
        elif ny <= 0:
            print("top edge")
            self.yspeed *= -1
            self.y = 1

            return [0, 0]

        # check if ball intersects at the bottom edge
        collision_point = col.get_segment_intersection(self.x, self.y, nx, ny + BALL_SIZE, bottom1[0], bottom1[1], bottom2[0], bottom2[1])
        if collision_point is not None:
            print("collision with bottom")
            self.yspeed *= -1
            self.y = collision_point[1]-BALL_SIZE-1

            return [0, 0]
        elif ny >= WINDOW_HEIGHT:
            self.yspeed *= -1
            self.y = WINDOW_HEIGHT-BALL_SIZE-1

            return [0, 0]

        
        # check if ball intersects at the right edge
        #collision_point = col.get_segment_intersection(self.x + BALL_SIZE, self.y, nx + BALL_SIZE, ny, top2[0], top2[1], bottom2[0], bottom2[1])
        #if collision_point is not None:
        if nx + BALL_SIZE >= WINDOW_WIDTH-WINDOW_MARGIN:
            # left player scored
            print("OOOOOOOOOOO")
            left_score += 1
            self.reset()

            return [1, 0]

        # check if ball intersects at the left edge
        #collision_point = col.get_segment_intersection(self.x, self.y, nx, ny, top1[0], top1[1], bottom1[0], bottom1[1])
        #if collision_point is not None:
        if nx <= WINDOW_MARGIN:
            # right player scored
            right_score += 1
            self.reset()

            return [0, 1]

        return [0, 0] # error
        



