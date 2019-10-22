import pygame 
import config
import logging
from client import Client

logging.basicConfig(
    filename="player.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


pygame.init()

window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Client")

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

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    pass

def make_pos():
    pass

def redrawWindow(player):
    window.fill((255,255,255))
    player.draw(window)
    pygame.display.update()


def main():
    run = True
    client = Client()
    player1 = Player(50, 50, 100, 100, (0,255,0))
    player2 = Player(50, 50, 100, 100, (255,255,0))

    clock = pygame.time.Clock()

    while(run):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        redrawWindow(player1)


if __name__ == "__main__":
    main()
