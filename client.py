import socket
import logging
import threading
from config import *
import pickle
from player import Player
from network import Client
import pygame

pygame.init()

logging.basicConfig(
    filename="client.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Client")


def redraw_window(player1, player2):
    window.fill(WHITE)
    player1.draw(window)
    player2.draw(window)

    pygame.display.update()


def main():
    run = True
    client = Client()

    player1 = client.get_player()

    clock = pygame.time.Clock()

    while(run):
        clock.tick(60)
        player2 = client.send(player1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        redraw_window(player1, player2)



if __name__ == "__main__":
    main()
