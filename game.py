from config import *
from player import Paddle
from client import Client
from ball import Ball 
import pygame
from log import Log
import time
import threading

""" Game states """
class States(Enum):
    STARTING = 1
    WAITING = 3

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
WAIT = False

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


def no_game_display():
    """ creates a reset screen """
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
        

def init_paddles(client):
    current_player = Paddle(client.recv_pos_msg())
    print("current pos: ", current_player.get_pos())

    opposite_player = Paddle(client.recv_pos_msg())
    print("opposite_pos: ", opposite_player.get_pos())

    return current_player, opposite_player


def main():
    # gets the initial state
    client = Client()

    handle_state(client)

    if START is True:
        start_pong(client)
    
    else:
        game_log.log(LogLevels.ERROR.value, "Game finished before start")
        client.close()
    

def handle_state(client):
    global WAIT, START

    initial_state = client.get_state()
    print("initial state = ", initial_state)

    if initial_state is States.WAITING.value:
        WAIT = True

        print("WAITING")

        timeout = client.recv_wait_msg()

        print("timeout: ", timeout)

        wait_thread = threading.Thread(target=wait, args=(client, timeout, ))
        wait_thread.start()

        wait_display(timeout) # timer

        wait_thread.join()
        
    elif initial_state is States.STARTING.value:
        start = client.recv_start_msg() # recv wait message with 0 timeout
        print("STARTING")

        if start == 0:
            START = True


def wait(client, timeout):
    global START

    if client.recv_msg_with_timeout(timeout) is False:
        game_log.log(LogLevels.ERROR.value, "Game finished while WAITING: no connection from other player")
        client.close()
        
        print("TIMEOUT")
    else:
        START = True

        print("received START from server")


def wait_display(seconds):
    global START

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

        return False
    
    else:
        return True


def start_pong(client):
    global WAIT, START

    clock = pygame.time.Clock()
    
    current_player, opposite_player = init_paddles(client)

    print("have players")

    # Game event
    run = True
    while(run):
        dt = clock.tick(FPS)

        print("rady to recv ball_pos")
        ball_pos = client.recv_pos_msg()
        print("ball_pos = ", ball_pos)
        
        score = client.recv_score_msg()
        
        opposite_pos = client.send_pos( current_player.get_pos() )
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
