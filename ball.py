import config
import math
import random
from log import Log
import pygame
import math
import random
import collision as col
from datetime import datetime
import sys

pygame.init()

random.seed(datetime.now())

class Ball():
    def __init__(self):
        self.x = config.WINDOW_WIDTH/2
        self.y = config.WINDOW_HEIGHT/2
        self.size = 10
        self.speed = 0.2
        self.xspeed = self.speed
        self.yspeed = self.speed

        self.rect = (self.x, self.y, self.size, self.size)

        self.reset()
        
    def reset(self):
        self.x = config.WINDOW_WIDTH/2
        self.y = config.WINDOW_HEIGHT/2

        angle = random.uniform(math.pi/4, -math.pi/4)

        self.xspeed = self.speed * math.cos(angle)
        self.yspeed = self.speed * math.sin(angle)

        if random.randrange(0, 1) < 0.5:
            self.xspeed *= -1

    def draw(self, window):
        pygame.draw.rect(window, (255,255,255), self.rect)

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
        paddle_height = config.PADDLE_SIZE[1]
        paddle_width = config.PADDLE_SIZE[0]

        collision_point = col.get_segment_intersection(self.x, self.y, nx, ny, paddle_x + paddle_width, paddle_y, paddle_x + paddle_width, paddle_y + paddle_height)
        if collision_point is not None:
            # https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
            print("collided with left paddle")

            # take diff from middle of paddle
            relative_intersection = (paddle_y + (paddle_height / 2)) - collision_point[1]
            normalized = relative_intersection / (paddle_height/2)

            angle = normalized * col.BOUNCE_ANGLE # multiply by acceleration here
    
            self.xspeed = self.speed * math.cos(angle)
            self.yspeed = self.speed * -math.sin(angle)

            self.x = paddle_x + paddle_width

            return True

        return False


    def check_paddle_right(self, paddle_x, paddle_y, nx, ny):
        paddle_height = config.PADDLE_SIZE[1]
        paddle_width = config.PADDLE_SIZE[0]

        collision_point = col.get_segment_intersection(self.x + self.size, self.y, nx + self.size, ny, paddle_x, paddle_y, paddle_x, paddle_y + paddle_height)
        if collision_point is not None:
            # https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
            print("collided with right paddle")

            # take diff from middle of paddle
            relative_intersection = (paddle_y + (paddle_height / 2)) - collision_point[1]
            normalized = relative_intersection / (paddle_height/2)

            angle = normalized * col.BOUNCE_ANGLE # multiply by acceleration here

            self.xspeed = self.speed * -math.cos(angle)
            self.yspeed = self.speed * -math.sin(angle)

            self.x = paddle_x - self.size - paddle_width

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
        collision_point = col.get_segment_intersection(self.x, self.y, nx, ny + self.size, bottom1[0], bottom1[1], bottom2[0], bottom2[1])
        if collision_point is not None:
            print("collision with bottom")
            self.yspeed *= -1
            self.y = collision_point[1]-self.size-1

            return [0, 0]
        elif ny >= config.WINDOW_HEIGHT:
            self.yspeed *= -1
            self.y = config.WINDOW_HEIGHT-self.size-1

            return [0, 0]

        
        # check if ball intersects at the right edge
        if nx + self.size >= config.WINDOW_WIDTH-config.WINDOW_MARGIN:
            # left player scored
            left_score += 1
            self.reset()
            print("left player scored")
            sys.exit(1)
            return [1, 0]
        
        # check if ball intersects at the left edge
        if nx <= config.WINDOW_MARGIN:
            # right player scored
            right_score += 1
            self.reset()
            print("right player scored")
            sys.exit(1)

            return [0, 1]

        return [0, 0] # error
        



