"""
PONG server
"""

import socket
import threading
import logging
from config import *
import sys
import pickle
from player import Player
from packet import *
import time

logging.basicConfig(
    filename="server.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("server")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("server.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

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

            logger.info("Initialized PONG server at {}:{}".format(ip, str(port)))
        except socket.error as e:
            logger.error("Socket error while binding: {}".format(e))
            sys.exit(1)

    def listen(self):
        global PLAYER_COUNT

        try:
            run = True
            while run:
                conn, addr = self.server.accept()
                PLAYER_COUNT += 1
                
                logger.info("Connection established with {}".format(addr))

                clients.append(conn)

                client_thread = threading.Thread(target=self.run_client, args=(conn, PLAYER_COUNT-1,))
                client_thread.start()
                
        except KeyboardInterrupt:
            logger.warning("Interrupted form keyboard")


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
                    logger.warning("Client {} disconnected".format(conn))
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
                logger.error("Error at run_client(): {}".format(e))
                sys.exit(1)
            

def main():
    pongServer = PongServer(LOCALHOST, PORT)
    pongServer.listen()
    

if __name__ == "__main__":
    main()
