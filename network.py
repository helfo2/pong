import socket
import logging
from config import *
import struct
import sys

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

            return pickle.loads(self.client.recv(BUFF_SIZE))
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))
            sys.exit(1)

    def make_pkt(self, msg_type, data):
        if msg_type == MsgTypes.POS.value:
            """ data is location type [x,y] """
            return struct.pack("Hii", msg_type, data[0], data[1])
        else:
            logging.warning("make_pkt: Dont know the type of message")

    def unmake_pkt(self, msg_type, pkt):
        if msg_type == MsgTypes.POS.value:
            """ data is location type [x,y] """
            msg = struct.unpack("Hii", pkt)

            return msg[1], msg[2] # x and y
        else:
            logging.warning("unmake_pkt: Dont know the type of message")

    def send(self, msg_type, data):
        try:
            pkt = self.make_pkt(msg_type, data)

            self.client.send(pkt)
            return pickle.loads(self.client.recv(BUFF_SIZE))
        except socket.error as e:
            logging.error("Error sending {}: {}".format(data, e))

    def send_position(self, pos):
        pass

    def get_player(self):
        return self.player
