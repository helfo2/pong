"""
PONG server
"""

import socket
from threading import Thread
import logging

LOCALHOST = "127.0.0.1"
PORT = 1234

MSS = 2048

class PongServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)

        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.clients = []

        logging.info("Initialized PONG server at {}:{}".format(ip, str(port)))

    def sendData(self, data, addr):
        logging.info("Sending {} to {}".format(str(data), addr))

        self.server.sendto("ok".encode(), addr)

    def listen(self):
        while(True):
            msg, client = self.server.recvfrom(MSS)
            logging.info("Received {} from {}".format(str(msg), client))

def main():
    logging.getLogger().setLevel(logging.DEBUG)

    pongServer = PongServer(LOCALHOST, PORT)
    pongServer.listen()
    
if __name__ == "__main__":
    main()


