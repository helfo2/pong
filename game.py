from config import *
from player import Paddle
from client import Client
from ball import Ball 
import pygame
from log import Log
import time

""" Game states """
class MsgTypes(Enum):
    WAIT = 1
    START = 2
    FINISH = 3

WINDOW_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
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

def create_text(text, position):
    text = font.render(str(text), True, WHITE, BLACK)
    text_rect = wait_text.get_rect()  
    text_rect.center = (position) 

    return text, text_rect
    

wait_text = font.render("waiting", True, WHITE, BLACK)
wait_text_rect = wait_text.get_rect()  
wait_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2) 


def is_flag_pos(pos):
    return pos[0] == -1 and pos[1] == -1


def redraw_window(player1, player2, ball_pos, score):
    global WINDOW_CENTER, SCORE1_POSITION, SCORE2_POSITION

    display_surface.fill(BLACK)
    player1.draw(display_surface)
    player2.draw(display_surface)
    
    # draw the ball
    pygame.draw.rect(display_surface, WHITE, (ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))

    # draw the net
    pygame.draw.line(display_surface, WHITE, [WINDOW_WIDTH/2, 0], [WINDOW_WIDTH/2, WINDOW_HEIGHT], 5)

    left_score_text, left_score_text_rect  = create_text(score[0], LEFT_SCORE_POSITION)
    

    # left_score_text = font.render(str(score[0]), True, WHITE, BLACK)   
    # left_score_text_rect = left_score_text.get_rect()  
    # left_score_text_rect.center = (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4) 

    right_score_text, right_score_text_rect  = create_text(score[1], RIGHT_SCORE_POSITION)

    # right_score_text = font.render(str(score[1]), True, WHITE, BLACK)
    # right_score_text_rect = right_score_text.get_rect()  
    # right_score_text_rect.center = (0.75 * WINDOW_WIDTH, WINDOW_HEIGHT // 4) 

    display_surface.blit(left_score_text, left_score_text_rect)
    display_surface.blit(right_score_text, right_score_text_rect)

    pygame.display.update()


def is_wait_state(time_wait):
    return time_wait is 0

def wait(seconds):
    count_seconds = 0
    while count_seconds < seconds:
        display_surface.fill(WHITE) 
    
        wait_text, wait_text_rect = create_text("waiting", WINDOW_CENTER)

        display_surface.blit(wait_text, wait_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
                game_log.log(LogLevels.INFO.value, "Game finished while WAITING")
                exit(0)

            pygame.display.update()

        time.sleep(1)
        count_seconds += 1        
        

        



def main():
    clock = pygame.time.Clock()

    # gets the initial state
    client = Client()

    initial_state = client.get_state()

    if is_wait_state(initial_state):
        
        
        time.sleep(initial_state)
    else:
        start_pong(client)
    




    current_player = Paddle(client.get_player_initial_pos())
    print(current_player.get_pos())

    # Wait event
    """ TODO
        try to use select here to no avoid polling over the network
    """
    wait = True
    while(wait):
        opposite_pos = client.recv_msg()
        
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


def start_pong(client):
    pass


if __name__ == "__main__":
    main()
