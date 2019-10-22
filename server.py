"""
PONG server
"""

import socket
from threading import Thread
import logging
import config
import sys

logging.basicConfig(filename="server.log", level=logging.DEBUG)

class PongServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        try:
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.server.bind((self.ip, self.port))
            self.clients = []
            
            logging.info("Initialized PONG server at {}:{}".format(ip, str(port)))
        except socket.error as e:
            logging.error("Socket error while binding: {}".format(e))

    def sendData(self, data, addr):
        logging.info("Sending {} to {}".format(str(data), addr))

        self.server.sendto("ok".encode(), addr)

    def listen(self):
        try:
            while(True):
                msg, client = self.server.recvfrom(config.MSS)
                logging.info("Received {} from {}".format(str(msg), client))
        except KeyboardInterrupt:
            logging.warning("Interrupted form keyboard")

def main():
    pongServer = PongServer(config.LOCALHOST, config.PORT)
    pongServer.listen()
    
if __name__ == "__main__":
    main()


