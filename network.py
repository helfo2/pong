import socket
import logging
from config import *
import pickle

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

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(BUFF_SIZE))
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))

    def get_player(self):
        return self.player
