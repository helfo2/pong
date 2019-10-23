"""
PONG server
"""

import socket
import threading
import logging
import config
import sys
import pickle

logging.basicConfig(
    filename="server.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

_pos = [(0,0), (100,100)]


def read_pos(pos):
    pos = pos.split(",")
    return int(pos[0]), int(pos[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) 


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
        conn.send(make_pos(_pos[player]).encode())

        while True:
            try:
                data = read_pos(conn.recv(config.BUFF_SIZE).decode())
                _pos[player] = data

                if not data:
                    logging.info("Client {} disconnected".format(conn))
                else:
                    if player == 1:
                        reply = _pos[0]
                    else:
                        reply = _pos[1]


                    print("Received: ", data)
                    logging.info("Received {} from {}".format(str(reply), conn))
                    print("Sending: ", reply)

                conn.sendall(make_pos(reply).encode())
            except Exception as e:
                logging.error("Error at run_client(): {}".format(e))
                sys.exit(1)
            

def main():
    pongServer = PongServer(config.LOCALHOST, config.PORT)
    pongServer.listen()
    

if __name__ == "__main__":
    main()
