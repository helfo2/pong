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
import errno

server_log = Log("server.log")

players_pos = [PLAYER_1_POS, PLAYER_2_POS]

player1_score = 0
player2_score = 0

player1_win = False
player2_win = False

PLAYER_COUNT = 0

ball = Ball()
clock = pygame.time.Clock()

class PongServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        try:
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.server.bind((self.ip, self.port))
            self.server.listen(2)

            server_log.log(LogLevels.INFO.value, "Initialized PONG server at {}:{}".format(ip, str(port)))
        except socket.error as e:
            server_log.log(LogLevels.ERROR.value, "Socket error while binding: {}".format(e))
            sys.exit(1)

    def listen(self):
        global PLAYER_COUNT

        try:
            run = True
            while run:
                conn, addr = self.server.accept()
                PLAYER_COUNT += 1
                
                server_log.log(LogLevels.INFO.value, "Connection established with {}".format(addr))

                client_thread = threading.Thread(target=self.run_client, args=(conn, PLAYER_COUNT-1,))
                client_thread.start()
                
        except KeyboardInterrupt:
            server_log.log(LogLevels.WARNING.value, "Interrupted form keyboard")


    def run_client(self, conn, player_num):
        global ball
        global clock

        print("player #:", player_num)
        print("player (x, y): {}".format(players_pos[player_num]))
        
        time.sleep(1)

        initial_pos = players_pos[player_num]

        # After connect, send initial position
        conn.send(make_pkt(MsgTypes.POS.value, initial_pos))

        # # Send a flag packet for synchronization
        # conn.send(make_pkt(MsgTypes.POS.value, FLAG_POS))

        # Tells player to wait for the other player
        while PLAYER_COUNT < 2:
            conn.send(make_pkt(MsgTypes.POS.value, FLAG_POS))

            time.sleep(0.5)

        reply = players_pos[not player_num]
        conn.send(make_pkt(MsgTypes.POS.value, reply))

        # Runs the game
        while True:
            try:
                dt = clock.tick(30)

                data = unmake_pkt(MsgTypes.POS.value, conn.recv(BUFF_SIZE))

                if not data:
                    server_log.log(LogLevels.WARNING.value, "Client {} disconnected".format(conn))
                else:
                    players_pos[player_num] = data
                
                reply = players_pos[not player_num]
                print("Sending: ", reply)
                conn.send(make_pkt(MsgTypes.POS.value, reply))
                
                # First, deal with collisions
                nx, ny = ball.try_update(dt)

                print("nx = ", nx)
                print("ny = ", ny)

                ball.edges(nx, ny)
                ball.check_paddle_left(players_pos[0][0], players_pos[0][1], nx, ny)
                #ball.check_paddle_right(players_pos[1][0], players_pos[1][1])

                ball.update(dt)

                ball_pos = ball.get_pos()
                print("server ball_pos = ", ball_pos)
                conn.send(make_pkt(MsgTypes.POS.value, ball_pos))

            except socket.error as se:
                if se.errno == errno.WSAECONNRESET:
                    server_log.log(LogLevels.WARNING.value, "A player left the game")
                    sys.exit(0)
                else:
                    server_log.log(LogLevels.ERROR.value, "Socket error: {}".format(se))
                    sys.exit(1)

            except KeyboardInterrupt:
                print("Finishing server...")
                socket.close()
                sys.exit(0)
                
            except Exception as e:
                print("Exception occurred at the server. Check logs")
                server_log.log(LogLevels.ERROR.value, "Error at run_client(): {}".format(e))
                sys.exit(1)
            

def main():
    pongServer = PongServer(SERVER_IP, PORT)
    pongServer.listen()
    

if __name__ == "__main__":
    main()
