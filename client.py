from config import *
from player import Player
from network import Client
import pygame

FPS = 30

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Client")

font = pygame.font.Font("freesansbold.ttf", 32) 
  
wait_text = font.render("Waiting for the other player...", True, WHITE, BLACK)   
wait_text_rect = wait_text.get_rect()  
wait_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2) 

def is_flag_pos(pos):
    return pos[0] == -1 and pos[1] == -1


def redraw_window(player1, player2):
    display_surface.fill(BLACK)
    player1.draw(display_surface)
    player2.draw(display_surface)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()

    # Gets the initial position
    client = Client()

    current_player = Player(client.get_player_initial_pos())
    print(current_player.get_pos())

    # Wait event
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
                exit(0)

            pygame.display.update()

    print("opposite_pos: ", opposite_pos)

    # opposite_pos = client.recv_pos()
    opposite_player = Player(opposite_pos)

    # Game event
    run = True
    while(run):
        dt = clock.tick(FPS)

        opposite_pos = client.send_pos(current_player.get_pos())
        print("player2_pos: ", opposite_pos)
        opposite_player.update(opposite_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        current_player.move(dt)

        print("player1_pos: ", current_player.get_pos())

        redraw_window(current_player, opposite_player)



if __name__ == "__main__":
    main()
