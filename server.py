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

logging.basicConfig(
    filename="server.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

location_player1 = [WINDOW_MARGIN, WINDOW_HEIGHT/2 - 100]
location_player2 = [WINDOW_WIDTH-WINDOW_MARGIN-PADDLE_SIZE[0], WINDOW_HEIGHT/2 - 100]

# players = [location_player1, location_player2]
players = [Player(location=location_player1,color=RED), Player(location=location_player2,color=BLUE)]

player1_win = False
player2_win = False

class PongServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        try:
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.server.bind((self.ip, self.port))
            self.clients = []
            self.server.listen(2)

            logging.info("Initialized PONG server at {}:{}".format(ip, str(port)))
        except socket.error as e:
            logging.error("Socket error while binding: {}".format(e))
            sys.exit(1)

    def listen(self):
        run = True
        current_player = 0

        try:
            while(run):
                conn, addr = self.server.accept()
                logging.info("Connection established with {}".format(addr))    
                client_thread = threading.Thread(target=self.run_client, args=(conn, current_player,))
                client_thread.start()

                current_player += 1

        except KeyboardInterrupt:
            logging.warning("Interrupted form keyboard")


    def run_client(self, conn, player):
        print("player #:", player)
        conn.send(pickle.dumps(players[player]))

        while True:
            try:
                data = pickle.loads(conn.recv(BUFF_SIZE))
                players[player] = data

                if not data:
                    logging.info("Client {} disconnected".format(conn))
                else:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]


                    print("Received: ", data)
                    logging.info("Received {} from {}".format(str(reply), conn))
                    print("Sending: ", reply)

                conn.sendall(pickle.dumps(reply))
            except Exception as e:
                logging.error("Error at run_client(): {}".format(e))
                sys.exit(1)
            

def main():
    pongServer = PongServer(LOCALHOST, PORT)
    pongServer.listen()
    

if __name__ == "__main__":
    main()
