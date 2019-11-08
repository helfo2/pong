from config import *
from math import *
from random import *
from log import Log
import pygame
import math
import random
import collision as col

pygame.init()

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


    def check_paddle_right(self, paddle_x, paddle_y):
        paddle_height = PADDLE_SIZE[1]
        paddle_width = PADDLE_SIZE[0]

        # if self.x < paddle_x + paddle_width and self.y < paddle_y + paddle_height and self.x + self.size > paddle_x and self.y + self.size > paddle_y:
        #     diff = self.y - (paddle_y - paddle_height/2)
        #     angle = interpolate(diff, 0, paddle_height, radians(225), radians(135))
        #     self.xspeed = 5 * cos(angle)
        #     self.yspeed = 5 * sin(angle)

        #     self.x = paddle_x - paddle_width/2 - self.size

        if self.y - self.size < paddle_y + paddle_height/2 and self.y + self.size > paddle_y - paddle_height/2 and (self.x + self.size > paddle_x - paddle_width/2):
            if self.x < paddle_x:
                diff = self.y - (paddle_y - paddle_height/2)
                angle = col.interpolate(diff, 0, paddle_height, radians(225), radians(135))
                self.xspeed = 0.2 * cos(angle)
                self.yspeed = 0.2 * sin(angle)

                self.x = paddle_x - paddle_width/2 - self.size

                return True

        return False

    def edges(self, nx, ny):
        left_score = 0
        right_score = 0

        p1 = [self.x, self.y]
        q1 = [nx, ny]

        top1 = col.LEFT_WINDOW_TOP
        top2 = col.RIGHT_WINDOW_TOP

        # check if ball intersects at the top edge
        if col.do_intersect(p1, q1, top1, top2):
        #collision_point = col.get_segment_intersection(self.x, self.y, nx, ny, top1[0], top1[1], top2[0], top2[1])
        #if collision_point is not None:
            print("top edge")
            self.yspeed *= -1
            self.y = 1

            return True

        p1 = [self.x, self.y + BALL_SIZE]
        q1 = [nx, ny + BALL_SIZE]

        bottom1 = col.LEFT_WINDOW_BOTTOM
        bottom2 = col.RIGHT_WINDOW_BOTTOM

        # check if ball intersects at the bottom edge
        if col.do_intersect(p1, q1, bottom1, bottom2):
            self.yspeed *= -1
            self.y = WINDOW_HEIGHT-BALL_SIZE

            return True

        # p1 = [self.x, self.y]
        # q1 = [nx, ny]

        # left1 = col.LEFT_WALL_TOP
        # left2 = col.LEFT_WALL_BOTTOM

        # # check if ball goes through left wall
        # if col.do_intersect(p1, q1, left1, left2):
        #     left_score += 1
        #     self.reset()

        # p1 = [self.x + BALL_SIZE, self.y]
        # q1 = [nx + BALL_SIZE, ny]

        # right1 = col.RIGHT_WALL_TOP
        # right2 = col.RIGHT_WALL_BOTTOM

        # # check if ball goes through right wall
        # if col.do_intersect(p1, q1, right1, right2):
        #     right_score += 1
        #     self.reset()

        if self.x - self.size > WINDOW_WIDTH:
            left_score += 1
            self.reset()

            return True

        if self.x + self.size < 0:
            right_score += 1
            self.reset()

            return True

        return False
        



