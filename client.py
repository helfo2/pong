import socket
from log import Log
from config import *
import struct
import sys
from packet import *

client_log = Log("client.log")

class Client():
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.serverAddr = (SERVER_IP, PORT)

        self.player_initial_pos = self.connect()

    def connect(self):
        try:
            self.client.connect(self.serverAddr)

            client_log.log(LogLevels.INFO.value, "Connected to {}".format(self.serverAddr))

            return self.recv_pos()

        except socket.error as e:
            client_log.log(LogLevels.ERROR.value, "Could not connect to {}: {}".format(self.serverAddr, e))
            sys.exit(1)

    def recv_pos(self):
        return unmake_pkt(MsgTypes.POS.value, self.client.recv(BUFF_SIZE))

    def send_pos(self, data):
        try:
            pkt = make_pkt(MsgTypes.POS.value, data)

            self.client.send(pkt)
            return unmake_pkt(MsgTypes.POS.value, self.client.recv(BUFF_SIZE))
            
        except socket.error as e:
            client_log.log(LogLevels.ERROR.value, "Error sending {}: {}".format(data, e))

    def get_player_initial_pos(self):
        return self.player_initial_pos
