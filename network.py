import socket
import logging
from config import *
import struct
import sys
from packet import *

logging.basicConfig(
    filename="client.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class Client():
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.serverAddr = (LOCALHOST, PORT)

        self.player_pos = self.connect()

    def connect(self):
        try:
            self.client.connect(self.serverAddr)

            logging.info("Connected to {}".format(self.serverAddr))

            return self.recv_pos()
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))
            sys.exit(1)

    def recv_pos(self):
        return unmake_pkt(MsgTypes.POS.value, self.client.recv(BUFF_SIZE))

    def send_pos(self, data):
        try:
            pkt = make_pkt(MsgTypes.POS.value, data)

            self.client.send(pkt)
            return unmake_pkt(MsgTypes.POS.value, self.client.recv(BUFF_SIZE))
        except socket.error as e:
            logging.error("Error sending {}: {}".format(data, e))

    def get_player_pos(self):
        return self.player_pos
