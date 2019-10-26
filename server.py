"""
PONG server
"""

import socket
import threading
from config import *
from log import Log
import sys
import pickle
from player import Player
from packet import *
import time

server_log = Log("server.log")

position_player1 = PLAYER_1_POS
position_player2 = PLAYER_2_POS

players_pos = [position_player1, position_player2]
#players = [Player(location=location_player1,color=RED), Player(location=location_player2,color=BLUE)]

player1_win = False
player2_win = False

PLAYER_COUNT = 0

clients = []

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
        print("player #:", player_num)
        print("player (x, y): {}".format(players_pos[player_num]))
        
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

        # Starts the game
        while True:
            try:
                data = unmake_pkt(MsgTypes.POS.value, conn.recv(BUFF_SIZE))

                if not data:
                    server_log.log(LogLevels.WARNING.value, "Client {} disconnected".format(conn))
                else:
                    players_pos[player_num] = data
                
                reply = players_pos[not player_num]
                conn.send(make_pkt(MsgTypes.POS.value, reply))


                # if player_num == 1:
                #     reply = players_pos[0]
                # else:
                #     reply = players_pos[1]

                # print("Received: ", data)
                print("Sending: ", reply)
            except Exception as e:
                server_log.log(LogLevels.ERROR.value, "Error at run_client(): {}".format(e))
                sys.exit(1)
            

def main():
    pongServer = PongServer(LOCALHOST, PORT)
    pongServer.listen()
    

if __name__ == "__main__":
    main()
