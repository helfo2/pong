import pygame
from config import *
from pygame.locals import *
import logging

pygame.init()

class Player():
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.width = PADDLE_SIZE[0]
        self.height = PADDLE_SIZE[1]
        
        self.color = WHITE
        self.rect = (self.x, self.y, self.width, self.height)
        self.vel = 0.5

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if (self.y - self.vel * dt > 0):
                self.y -= self.vel * dt
            else:
                self.y = 1


        if keys[pygame.K_DOWN]:
            if (self.y + self.vel * dt + self.height < WINDOW_HEIGHT):
                self.y += self.vel * dt
            else:
                self.y = WINDOW_HEIGHT - self.height - 1

        self.update_internal()

    def update(self, pos):
        self.x = pos[0]
        self.y = pos[1]

        self.update_internal()

    def update_internal(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def get_pos(self):
        return [self.x, self.y]

