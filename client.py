import pygame 

import socket
import logging
import threading
import config

logging.basicConfig(
    filename="client.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

pygame.init()

pongClient = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
pongClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0  

class Client():
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.serverAdrr = (config.LOCALHOST, config.PORT)

        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.serverAdrr)
            return self.client.recv(config.BUFF_SIZE).decode()
        except Exception as e:
            pass



class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)

def redrawWindow(player):
    window.fill((255,255,255))
    player.draw(window)
    pygame.display.update()


def main():
    run = True
    player = Player(50, 50, 100, 100, (0,255,0))


    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        redrawWindow(player)

    pongClient.sendto("hello".encode(), (config.LOCALHOST, config.PORT))

if __name__ == "__main__":
    main()