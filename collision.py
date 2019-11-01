from math import *
from random import *
from config import *

def interpolate(value, start, end, new_start, new_end):
    return new_start + (new_end - new_start) * ((value - start) / (end - start))

def reset_ball():
    x = WINDOW_WIDTH/2
    y = WINDOW_HEIGHT/2

    angle = uniform(-pi/4, pi/4)

    xspeed = 5 * cos(angle)
    yspeed = 5 * sin(angle)

    if randrange(1) < 0.5:
        xspeed *= -1

    return (x, y, xspeed, yspeed)

def check_paddle_left(self, ball_x, ball_y, paddle_x, paddle_y):
    paddle_height = PADDLE_SIZE[1]
    paddle_width = PADDLE_SIZE[0]

    if (ball_y - self.size < paddle_y + paddle_height/2) and (ball_y + self.size > paddle_y - paddle_height/2) and self.x - self.size < paddle_x + paddle_width/2:
        if x > paddle_x:
            diff = ball_y - (paddle_y - paddle_height/2)
            rad = radians(45)
            angle = interpolate(diff, 0, paddle_height, -rad, rad)
            self.xspeed = 5 * cos(angle)
            self.yspeed = 5 * sin(angle)

            self.x = paddle_x + paddle_width/2 + self.size


def check_paddle_right(self, paddle_x, paddle_y):
    paddle_height = PADDLE_SIZE[1]
    paddle_width = PADDLE_SIZE[0]

    if self.y - self.size < paddle_y + paddle_height/2 and self.y + self.size > paddle_y - paddle_height/2 and (self.x + self.size > paddle_x - paddle_width/2):
        if self.x < paddle_x:
            diff = self.y - (paddle_y - paddle_height/2)
            angle = interpolate(diff, 0, paddle_height, radians(225), radians(135))
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