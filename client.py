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

    player1_pos = client.get_player_pos()
    player1 = Player(player1_pos, RED)

    player2 = Player(PLAYER_2_POS, BLUE)

    print("player1 = ", player1_pos)

    clock = pygame.time.Clock()

    while(run):
        clock.tick(60)
        player2_pos = client.send_pos(player1_pos)
        print("player2_pos: ", player2_pos)
        player2.update(player2_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()

        print("player1_pos: ", player1.get_pos())

        redraw_window(player1, player2)



if __name__ == "__main__":
    main()
