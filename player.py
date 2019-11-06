import pygame
from config import *
from pygame.locals import *
import logging

pygame.init()

# class Paddle(pygame.sprite.Sprite):
#     def __init__(self, number, color):
#         pygame.sprite.Sprite.__init__(self)

#         self.player_number = number
        
#         # Creates paddle image
#         self.image = pygame.Surface(PADDLE_SIZE)
#         self.image.fill(color)
#         self.rect = self.image.get_rect() # Now we can update x and y

#         self.speed = PADDLE_SPEED


#     def set_locations(self, surface):
#         if self.player_number == 1:
#             self.rect.centerx = surface.get_rect()
#             self.rect_centerx += 50
#         elif self.player_number == 2:
#             self.rect.centerx = surface.get_rect()
#             self.rect_centerx -= 50
        
#         self.rect.centery = surface.get_rect().centery

#     def move(self):
#         # Gets latest state of keyboard
#         pygame.event.pump()

#         # Gets current pressed key, independs of the frame
#         keys = pygame.key.get_pressed()

#         if keys[pygame.K_UP] and (self.rect.y > WINDOW_MARGIN):
#             self.rect.y -= self.speed
#         elif keys[pygame.K_DOWN] and (self.rect.bottom < WINDOW_HEIGHT-WINDOW_MARGIN):
#             self.rect.y += self.speed

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
            if (self.y - self.vel * dt > WINDOW_MARGIN):
                self.y -= self.vel * dt
            else:
                self.y = WINDOW_MARGIN


        if keys[pygame.K_DOWN]:
            if (self.y + self.vel * dt + self.height < WINDOW_HEIGHT-WINDOW_MARGIN):
                self.y += self.vel * dt
            else:
                self.y = WINDOW_HEIGHT-WINDOW_MARGIN - self.height

        self.update_internal()

    def update(self, pos):
        self.x = pos[0]
        self.y = pos[1]

        self.update_internal()

    def update_internal(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def get_pos(self):
        return [self.x, self.y]

