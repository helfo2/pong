from config import *
from log import Log
import pygame
from math import *
from random import *

pygame.init()


def _map_new_range(value, start, end, new_start, new_end):
    return new_start + (new_end - new_start) * ((value - start) / (end - start))


class Ball():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = BALL_LEN
        self.color = WHITE
        self.rect = (x, y, self.size, self.size)

        self.reset()
        
    def reset(self):
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2

        angle = random(-pi/4, pi/4)

        self.xspeed = 5 * cos(angle)
        self.yspeed = 5 * sin(angle)

        if random(1) < 0.5:
            self.xspeed *= -1

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def update(self):
        self.x += self.xspeed
        self.y += self.yspeed
    
        self.rect = (self.x, self.y, self.size, self.size)

    def check_paddle_left(self, paddle_x, paddle_y):
        paddle_height = PADDLE_SIZE[1]
        paddle_width = PADDLE_SIZE[0]

        if (self.y - self.size < paddle_y + paddle_height/2) and (self.y + self.size > paddle_y - paddle_height/2) and self.x - self.size < paddle_x + paddle_width/2:
            if x > paddle_x:
                diff = self.y - (paddle_y - paddle_height/2)
                rad = radians(45)
                angle = _map_new_range(diff, 0, paddle_height, -rad, rad)
                self.xspeed = 5 * cos(angle)
                self.yspeed = 5 * sin(angle)

                self.x = paddle_x + paddle_width/2 + self.size


    def check_paddle_right(self, paddle_x, paddle_y):
        paddle_height = PADDLE_SIZE[1]
        paddle_width = PADDLE_SIZE[0]

        if self.y - self.size < paddle_y + paddle_height/2 and self.y + self.size > paddle_y - paddle_height/2 and (self.x + self.size > paddle_x - paddle_width/2):
            if self.x < paddle_x:
                diff = self.y - (paddle_y - paddle_height/2)
                angle = _map_new_range(diff, 0, paddle_height, radians(225), radians(135))
                self.xspeed = 5 * cos(angle)
                self.yspeed = 5 * sin(angle)

                self.x = paddle_x - paddle_width/2 - self.size


    def edges(self):
        left_score = 0
        right_score = 0

        if self.y < 0 or self.y > WINDOW_HEIGHT:
            yspeed *= -1

        if self.x - self.size > WINDOW_WIDTH:
            left_score += 1
            self.reset()

        if self.x + self.size < 0:
            right_score += 1
            self.reset()

        return (left_score, right_score)
        



