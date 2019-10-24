import socket
import logging
from config import *
import struct
import sys
from packet import Packet

logging.basicConfig(
    filename="client.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class Client():
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.serverAddr = (LOCALHOST, PORT)

        self.player = self.connect()

    def connect(self):
        try:
            self.client.connect(self.serverAddr)

            logging.info("Connected to {}".format(self.serverAddr))

            return self.unmake_pkt(self.client.recv(BUFF_SIZE))
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))
            sys.exit(1)

    def send(self, msg_type, data):
        try:
            pkt = self.make_pkt(msg_type, data)

            self.client.send(pkt)
            return self.unmake_pkt(self.client.recv(BUFF_SIZE))
        except socket.error as e:
            logging.error("Error sending {}: {}".format(data, e))

    def send_position(self, pos):
        pass

    def get_player(self):
        return self.player
