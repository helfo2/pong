import socket
from log import Log
import config
import struct
import sys
import packet
import select

client_log = Log("client.log")

class Client():
    def __init__(self):
        self.serverAddr = (config.SERVER_IP, config.PORT)
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        
        self.state = self.connect()

    def connect(self):
        try:
            self.client.connect(self.serverAddr)

            client_log.log(config.LogLevels.INFO.value, "Connected to {}".format(self.serverAddr))

            return self.recv_msg()

        except socket.error as e:
            client_log.log(config.LogLevels.ERROR.value, "Could not connect to {}: {}".format(self.serverAddr, e))
            sys.exit(1)

    def recv_msg(self):
        # raw_msg = self.recv_all(2)
        # if not raw_msg:
        #     return None

        # msg_type = struct.unpack("H", raw_msg)[0]

        # msg_sz = packet.msg_size_from_type(msg_type)

        # msg = self.recv_all(msg_sz)

        data = packet.unmake_pkt(self.client.recv(config.BUFF_SIZE))

        return data

    def recv_msg_timeout(self, timeout):
        """ Deals with the start of the game """
        ready = select.select([self.client], [], [], timeout)

        if ready[0]:
            data = packet.unmake_pkt(self.client.recv(config.BUFF_SIZE))

            if data == 0:
                return True
            else: # error, only accepted payload for START is zero
                return False
    
    def recv_all(self, n):
        data = bytearray()

        while len(data) < n:
            packet = self.client.recv(n-len(data))
            print("packet ", packet)
            if not packet:
                return None

            data.extend(packet)

        return data


    def send_pos(self, data):
        try:
            pkt = packet.make_pkt(config.MsgTypes.POS.value, data)

            self.client.send(pkt)
            return self.recv_msg()
            
        except socket.error as e:
            client_log.log(config.LogLevels.ERROR.value, "Error sending {}: {}".format(data, e))

    def get_state(self):
        return self.state

    def close(self):
        self.client.close()
