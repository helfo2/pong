"""
PONG server
"""

import socket
import threading
from config import *
from log import Log
import sys
from packet import *
import time
from ball import Ball
import collision
import pygame 

server_log = Log("server.log")

FPS = 30

WAIT_SECOND_PLAYER_TIME = 10

""" Initial locations """
PLAYER_1_POS = [float(WINDOW_MARGIN), float(WINDOW_HEIGHT/2 - 100)]
PLAYER_2_POS = [float(WINDOW_WIDTH-WINDOW_MARGIN-PADDLE_SIZE[0]), float(WINDOW_HEIGHT/2 - 100)]
FLAG_POS = [-1.0,-1.0]

players_pos = [PLAYER_1_POS, PLAYER_2_POS]

player1_score = 0
player2_score = 0

player1_win = False
player2_win = False

PLAYER_COUNT = 0

clock = pygame.time.Clock()

SCORE = [0, 0]

class PongServer():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connected_clients = []

        try:
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.server.bind((self.ip, self.port))
            self.server.listen(3)

            server_log.log(LogLevels.INFO.value, "Initialized PONG server at {}:{}".format(ip, str(port)))

        except socket.error as e:
            server_log.log(LogLevels.ERROR.value, "Socket error while binding: {}".format(e))
            self.server.close()
            sys.exit(1)


    def listen(self):
        server_log.log(LogLevels.INFO.value, "Listening...")

        try:
            run = True
            while run:
                conn, addr = self.server.accept()
                                
                self.add_client(conn)

                self.try_run_game()

                server_log.log(LogLevels.INFO.value, "Connection established with {}".format(addr))
                
        except KeyboardInterrupt:
            server_log.log(LogLevels.WARNING.value, "Interrupted form keyboard")


    def add_client(self, client):
        global PLAYER_COUNT
        
        self.connected_clients.append(client)
        PLAYER_COUNT += 1


    def try_run_game(self):
        global PLAYER_COUNT

        if PLAYER_COUNT == 2:
            self.run_game()
        
        elif PLAYER_COUNT < 2: # only one player, tells it to wait
            self.send_wait_msg(self.connected_clients[0])

        else:
            server_log.log(LogLevels.ERROR.value, "Can't handle more than two connections")


    def run_game(self):
        ball = Ball()

        threads = []
        for conn_id, conn in enumerate(self.connected_clients):
            threads.append( threading.Thread(target=self.run_client, args=(conn, conn_id, ball, )) )
            
        for t in threads:    
            t.start()


    def send_wait_msg(self, conn):
        global WAIT_SECOND_PLAYER_TIME

        conn.send(make_pkt(MsgTypes.WAIT.value, WAIT_SECOND_PLAYER_TIME))


    def update_score(self, score):
        global SCORE

        SCORE[0] += score[0]
        SCORE[1] += score[1]


    def game_end(self):
        return SCORE[0] == 15 or SCORE[1] == 15


    def send_start(self, conn):
        """ Tells game that it can start since there are two players """

        print("start sent ")

        conn.send(make_pkt(config.MsgTypes.START.value))


    def send_initial_positions(self, conn, player_num):
        """ After starting the game, send initial position of both players """

        initial_pos = players_pos[player_num]

        print("sending initial position of ", initial_pos)
        conn.send(make_pkt(MsgTypes.POS.value, initial_pos))

        opposite_pos = players_pos[not player_num]
        conn.send(make_pkt(MsgTypes.POS.value, opposite_pos))


    def run_client(self, conn, player_num, ball):
        import errno
        global clock, players_pos, SCORE

        self.send_start(conn)        

        print("player #:", player_num)
        print("player (x, y): {}".format(players_pos[player_num]))
        
        self.send_initial_positions(conn, player_num)

        # Runs the game
        run = True
        while run:
            try:
                dt = clock.tick(FPS)

                # if self.game_end():
                #     conn.send()

                # First, deal with collisions
                nx, ny = ball.try_update(dt)

                print("nx = ", nx)
                print("ny = ", ny)

                ball.check_paddle_left(players_pos[0][0], players_pos[0][1], nx, ny)
                ball.check_paddle_right(players_pos[1][0], players_pos[1][1], nx, ny)
                score = ball.edges(nx, ny)

                ball.update(dt)

                ball_pos = ball.get_pos()
                print("server ball_pos = ", ball_pos)
                conn.send(make_pkt(MsgTypes.POS.value, ball_pos))
                
                self.update_score(score)

                conn.send(make_pkt(MsgTypes.SCORE.value, SCORE))

                data = unmake_pkt(conn.recv(BUFF_SIZE))

                if not data:
                    server_log.log(LogLevels.WARNING.value, "Client {} disconnected with no data".format(conn))
                else:
                    players_pos[player_num] = data
                
                opposite_pos = players_pos[not player_num]
                print("Sending: ", opposite_pos)
                conn.send(make_pkt(MsgTypes.POS.value, opposite_pos))
                
            except socket.error as se:
                if se.errno == errno.WSAECONNRESET:
                    server_log.log(LogLevels.WARNING.value, "Client disconnected: {} | Exception: {}".format(conn, se))
                else:
                    server_log.log(LogLevels.ERROR.value, "Socket error: {}".format(se))
                conn.close()
                self.server.close()
                sys.exit(1)

            except KeyboardInterrupt:
                print("Finishing server from Keyboard...")
                self.server.close()
                sys.exit(0)
                
            except Exception as e:
                print("Exception occurred at the server. Check logs")
                server_log.log(LogLevels.ERROR.value, "Error at run_client(): {}".format(e))
                self.server.close()
                sys.exit(1)


def main():
    pongServer = PongServer(SERVER_IP, PORT)
    pongServer.listen()
    

if __name__ == "__main__":
    main()
