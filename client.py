import socket
import logging
import threading
import config
import pickle

logging.basicConfig(
    filename="client.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


clientNumber = 0  

class Client():
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.serverAddr = (config.LOCALHOST, config.PORT)

        self.pos = self.connect()

    def connect(self):
        try:
            self.client.connect(self.serverAddr)

            logging.info("Connected to {}".format(self.serverAddr))

            #return self.client.recv(config.BUFF_SIZE).decode()
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return self.client.recv(config.BUFF_SIZE).decode()
        except socket.error as e:
            logging.error("Could not connect to {}: {}".format(self.serverAddr, e))

    def get_pos(self):
        return self.pos


def main():
    client = Client()

    client.send("teste1")


if __name__ == "__main__":
    main()
