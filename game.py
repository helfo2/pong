from config import *
from player import Paddle
from client import Client
from ball import Ball 
import pygame
from log import Log

game_log = Log("game.log")

FPS = 30

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Client")

font = pygame.font.Font("arcadeclassic-font/ARCADECLASSIC.TTF", 32) 
  
wait_text = font.render("Waiting for the other player...", True, BLACK, WHITE)   
wait_text_rect = wait_text.get_rect()  
wait_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2) 

def is_flag_pos(pos):
    return pos[0] == -1 and pos[1] == -1

def redraw_window(player1, player2, ball_pos):
    display_surface.fill(BLACK)
    player1.draw(display_surface)
    player2.draw(display_surface)
    
    # draw the ball
    pygame.draw.rect(display_surface, WHITE, (ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))

    # draw the net
    pygame.draw.line(display_surface, WHITE, [WINDOW_WIDTH/2, 0], [WINDOW_WIDTH/2, WINDOW_HEIGHT], 5)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()

    # gets the initial position
    client = Client()

    current_player = Paddle(client.get_player_initial_pos())
    print(current_player.get_pos())

    # Wait event
    """ TODO
        try to use select here to no avoid polling over the network
    """
    wait = True
    while(wait):
        opposite_pos = client.recv_pos()
        
        # if opposite_pos is [-1,-1]
        if not is_flag_pos(opposite_pos):
            print("Wait stopped")
            wait = False 
            break

        display_surface.fill(WHITE) 
  
        display_surface.blit(wait_text, wait_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_log.log(LogLevels.INFO.value, "Game finished while WAITING")
                exit(0)

            pygame.display.update()

    print("opposite_pos: ", opposite_pos)

    # opposite_pos = client.recv_pos()
    opposite_player = Paddle(opposite_pos)

    # Game event
    run = True
    while(run):
        dt = clock.tick(FPS)

        ball_pos = client.recv_pos()
        print("ball_pos = ", ball_pos)

        opposite_pos = client.send_pos(current_player.get_pos())
        print("player2_pos: ", opposite_pos)
        opposite_player.update(opposite_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                game_log.log(LogLevels.INFO.value, "Game finished")
                exit(0)

        current_player.move(dt)

        print("player1_pos: ", current_player.get_pos())
        
        redraw_window(current_player, opposite_player, ball_pos)



if __name__ == "__main__":
    main()
