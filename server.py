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
from queue import Queue

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
lock = threading.RLock()

SCORE = [0, 0]

queue = Queue()

class PongServer():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connected_clients = []
        self.ball = Ball()

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


    def add_client(self, conn):
        global PLAYER_COUNT

        self.send_initial_state(conn)

        self.connected_clients.append(conn)

        PLAYER_COUNT += 1

        
    def send_initial_state(self, conn):
        global PLAYER_COUNT

        if PLAYER_COUNT == 0:
            # the first player, no other waiting
            conn.send(make_pkt(MsgTypes.STATE.value, States.WAITING.value))
        else:
            # the second player, already other player waiting
            conn.send(make_pkt(MsgTypes.STATE.value, States.STARTING.value))


    def try_run_game(self):
        global PLAYER_COUNT

        if PLAYER_COUNT == 2:
            self.run_game()
        
        elif PLAYER_COUNT == 1: # only one player, tells it to wait
            self.send_wait_msg(self.connected_clients[0])

        else:
            server_log.log(LogLevels.ERROR.value, "Can't handle more than two connections")


    def run_game(self):
        threading.Thread(target=self.produce_game_events, ).start()

        threads = []
        for conn_id, conn in enumerate(self.connected_clients):
            threads.append( threading.Thread(target=self.run_client2, args=(conn, conn_id, )) )
            
        for t in threads:    
            t.start()


    def send_wait_msg(self, conn):
        global WAIT_SECOND_PLAYER_TIME

        conn.send(make_pkt(MsgTypes.WAIT.value, WAIT_SECOND_PLAYER_TIME))


    def update_score(self, score):
        global lock

        with lock:
            global SCORE

            SCORE[0] += score[0]
            SCORE[1] += score[1]


    def game_end(self):
        return SCORE[0] == 15 or SCORE[1] == 15


    def send_start(self, conn):
        """ Tells game that it can start since there are two players """

        print("start sent ")

        conn.send(make_pkt(MsgTypes.START.value))


    def send_initial_positions(self, conn, player_num):
        """ After starting the game, send initial position of both players """
        initial_pos = players_pos[player_num]

        print("sending initial position of ", initial_pos)
        conn.send(make_pkt(MsgTypes.POS.value, initial_pos))

        opposite_pos = players_pos[not player_num]
        conn.send(make_pkt(MsgTypes.POS.value, opposite_pos))

    
    def produce_game_events(self):
        global queue

        # Runs the game
        run = True
        dt = FPS
        while run:
            print("dt = ", dt)

            # if self.game_end():
            #     conn.send()

            # First, deal with collisions
            nx, ny = self.ball.try_update(dt)

            print("nx = ", nx)
            print("ny = ", ny)

            lock.acquire()

            self.ball.check_paddle_left(players_pos[0][0], players_pos[0][1], nx, ny)
            self.ball.check_paddle_right(players_pos[1][0], players_pos[1][1], nx, ny)
            score = self.ball.edges(nx, ny)

            self.ball.update(dt)

            ball_pos = self.ball.get_pos()

            lock.release()

            queue.put(ball_pos)

            lock.acquire()

            self.update_score(score)

            lock.release()

            queue.put(SCORE)

            dt = clock.tick(FPS)

    
    def run_client2(self, conn, player_num):
        """ Consumes game events and sends them all to the each client """

        import errno
        global queue, players_pos, SCORE

        self.send_start(conn)        

        print("player #:", player_num)
        print("player (x, y): {}".format(players_pos[player_num]))
        
        self.send_initial_positions(conn, player_num)

        print("ball position = ", self.ball.get_pos())
        
        # Runs the game
        run = True
        dt = FPS
        while run:
            try:
                print("dt = ", dt)

                # if self.game_end():
                #     conn.send()

                # First, deal with collisions

                ball_pos = queue.get()

                print("server ball_pos = ", ball_pos)
                conn.send(make_pkt(MsgTypes.POS.value, ball_pos))
                
                score = queue.get()

                print("score = ", score)

                conn.send(make_pkt(MsgTypes.SCORE.value, score))

                data = unmake_pkt(conn.recv(POS_MSG_SIZE))

                if not data:
                    server_log.log(LogLevels.WARNING.value, "Client {} disconnected with no data".format(conn))
                else:
                    lock.acquire()
                    players_pos[player_num] = data
                    lock.release()
               
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



    def run_client(self, conn, player_num):
        """ Consumes game events and sends them all to the each client """

        import errno
        global lock, players_pos, SCORE

        self.send_start(conn)        

        print("player #:", player_num)
        print("player (x, y): {}".format(players_pos[player_num]))
        
        self.send_initial_positions(conn, player_num)

        print("ball position = ", self.ball.get_pos())
        
        # Runs the game
        run = True
        dt = FPS
        while run:
            try:
                print("dt = ", dt)

                # if self.game_end():
                #     conn.send()

                # First, deal with collisions

                nx, ny = self.ball.try_update(dt)

                print("nx = ", nx)
                print("ny = ", ny)

                self.ball.check_paddle_left(players_pos[0][0], players_pos[0][1], nx, ny)
                self.ball.check_paddle_right(players_pos[1][0], players_pos[1][1], nx, ny)
                score = self.ball.edges(nx, ny)

                self.ball.update(dt)

                ball_pos = self.ball.get_pos()

                print("server ball_pos = ", ball_pos)
                conn.send(make_pkt(MsgTypes.POS.value, ball_pos))
                
                self.update_score(score)

                conn.send(make_pkt(MsgTypes.SCORE.value, SCORE))

                data = unmake_pkt(conn.recv(POS_MSG_SIZE))

                if not data:
                    server_log.log(LogLevels.WARNING.value, "Client {} disconnected with no data".format(conn))
                else:
                    players_pos[player_num] = data
               
                opposite_pos = players_pos[not player_num]

                print("Sending: ", opposite_pos)
                conn.send(make_pkt(MsgTypes.POS.value, opposite_pos))
                
                dt = clock.tick(FPS)
                
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
