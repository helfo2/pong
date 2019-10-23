import socket
import logging
import threading
import config
import pickle
from player import Player
import pygame

pygame.init()

logging.basicConfig(
    filename="client.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

""" Colors """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

""" Window """
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

PADDLE_SPEED = 10


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Client")


class Client():
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.serverAddr = (config.LOCALHOST, config.PORT)

        self.pos = self.connect()
        print("pos = {}".format(self.pos))

    def connect(self):
        try:
            self.client.connect(self.serverAddr)

            logging.info("Connected to {}".format(self.serverAddr))

            return self.client.recv(config.BUFF_SIZE).decode()
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))

    def send(self, data):
        try:
            self.client.send(data.encode())
            return self.client.recv(config.BUFF_SIZE).decode()
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))

    def get_pos(self):
        return self.pos


def read_pos(pos):
    pos = pos.split(",")
    return int(pos[0]), int(pos[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) 


def redrawWindow(player1, player2):
    window.fill((255,255,255))
    player1.draw(window)
    player2.draw(window)

    pygame.display.update()


def main():
    run = True
    client = Client()

    test = client.get_pos()
    print("pos from client: {}".format(test))

    start_pos = read_pos(test)

    player1 = Player(start_pos[0], start_pos[1], 100, 100, (0,255,0))
    player2 = Player(0, 0, 100, 100, (255,255,0))

    clock = pygame.time.Clock()

    while(run):
        clock.tick(60)

        player2_pos = read_pos(client.send(make_pos((player1.x, player1.y))))

        player2.x = player2_pos[0]
        player2.y = player2_pos[1]
        player2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        redrawWindow(player1, player2)



if __name__ == "__main__":
    main()
