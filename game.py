from config import *
from player import Paddle
from client import Client
from ball import Ball 
import pygame
from log import Log
import time
import threading

""" Game states """
class MsgTypes(Enum):
    WAIT = 1
    START = 2
    FINISH = 3

WINDOW_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
BELLOW_WINDOW_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
LEFT_SCORE_POSITION = (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4)
RIGHT_SCORE_POSITION = (0.75 * WINDOW_WIDTH, WINDOW_HEIGHT // 4) 

game_log = Log("game.log")

""" Colors """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 30

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Client")

font = pygame.font.Font("arcadeclassic-font/ARCADECLASSIC.TTF", 32) 

START = False

def create_text(text, position):
    """ Creates text and text rect objets to write on game window """
    text = font.render(str(text), True, WHITE, BLACK)
    text_rect = text.get_rect()  
    text_rect.center = (position) 

    return text, text_rect
    

def redraw_window(player1, player2, ball_pos, score):
    global WINDOW_CENTER, LEFT_SCORE_POSITION, RIGHT_SCORE_POSITION

    # draw background
    display_surface.fill(BLACK)

    # draw players
    player1.draw(display_surface)
    player2.draw(display_surface)
    
    # draw the ball
    pygame.draw.rect(display_surface, WHITE, (ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))

    # draw the net
    pygame.draw.line(display_surface, WHITE, [WINDOW_WIDTH/2, 0], [WINDOW_WIDTH/2, WINDOW_HEIGHT], 5)

    # draw score texts
    left_score_text, left_score_text_rect  = create_text(score[0], LEFT_SCORE_POSITION)
    display_surface.blit(left_score_text, left_score_text_rect)

    right_score_text, right_score_text_rect  = create_text(score[1], RIGHT_SCORE_POSITION)
    display_surface.blit(right_score_text, right_score_text_rect)

    pygame.display.update()


def is_wait_state(time_wait):
    return time_wait is not 0


def wait_display(seconds):
    global START, INTERRUPT

    counter = seconds
    while START is False and counter > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
                game_log.log(LogLevels.INFO.value, "Game finished while WAITING by user")

        display_surface.fill(BLACK) 

        wait_text, wait_text_rect = create_text("waiting", WINDOW_CENTER)
        seconds_text, seconds_text_rect = create_text(str(counter), BELLOW_WINDOW_CENTER)

        display_surface.blit(wait_text, wait_text_rect)
        display_surface.blit(seconds_text, seconds_text_rect)

        pygame.display.flip()

        counter -= 1
        time.sleep(1)

    if counter == 0: # no other player joined the match
        no_game_display()


def no_game_display():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
                game_log.log(LogLevels.INFO.value, "Game finished: no game")
                exit(0)
                
        display_surface.fill(BLACK) 

        text, text_rect = create_text("reset", WINDOW_CENTER)
        
        display_surface.blit(text, text_rect)

        pygame.display.flip()


def wait_server(client, timeout):
    global START

    if client.recv_msg_timeout(timeout) is not True:
        game_log.log(LogLevels.ERROR.value, "Game finished while WAITING: no connection from other player")
        client.close()
        
    else:
        START = True
        

def init_paddles(client):
    current_player = Paddle(client.recv_msg())
    print("current pos: ", current_player.get_pos())

    opposite_player = Paddle(client.recv_msg())
    print("opposite_pos: ", opposite_player.get_pos())

    return current_player, opposite_player


def main():
    clock = pygame.time.Clock()

    # gets the initial state
    client = Client()

    initial_state = client.get_state()
    
    if is_wait_state(initial_state):
        wait_server_thread = threading.Thread(target=wait_server, args=(client, initial_state, ))
        wait_server_thread.start()

        wait_display(initial_state)

    else:
        start_pong(client)
    

def start_pong(client):
    if START:
        current_player, opposite_player = init_paddles(client)

        # Game event
        run = True
        while(run):
            dt = clock.tick(FPS)

            ball_pos = client.recv_msg()
            print("ball_pos = ", ball_pos)

            score = client.recv_msg()

            opposite_pos = client.send_pos(current_player.get_pos())
            print("player2_pos: ", opposite_pos)
            opposite_player.update(opposite_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    client.close()
                    pygame.quit()
                    game_log.log(LogLevels.INFO.value, "Game finished")
                    exit(0)

            current_player.move(dt)

            print("player1_pos: ", current_player.get_pos())
            
            redraw_window(current_player, opposite_player, ball_pos, score)


if __name__ == "__main__":
    main()
