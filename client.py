import socket
from log import Log
import config
import struct
import sys
import packet
import select
import traceback

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

            return self.recv_state_msg()

        except socket.error as e:
            client_log.log(config.LogLevels.ERROR.value, "Could not connect to {}: {}".format(self.serverAddr, e))
            sys.exit(1)


    def recv_state_msg(self):
        return packet.unmake_pkt(self.client.recv(config.STATE_MSG_SIZE))

    def recv_wait_msg(self):
        return packet.unmake_pkt(self.client.recv(config.WAIT_MSG_SIZE))

    def recv_start_msg(self):
        return packet.unmake_pkt(self.client.recv(config.START_MSG_SIZE))

    def recv_pos_msg(self):
        test = packet.unmake_pkt(self.client.recv(config.POS_MSG_SIZE))
        print("waiting BALL msg: ", test)

        return test

    def recv_score_msg(self):
        return packet.unmake_pkt(self.client.recv(config.POS_MSG_SIZE))

    def recv_msg_with_timeout(self, timeout):
        """ Deals with the start of the game """
        try:
            ready, _ , _ = select.select([self.client], [], [], timeout)

            if ready:
                data = self.recv_start_msg()
                
                # self.client.send(packet.make_pkt(config.MsgTypes.START_ACK.value))
                # print("data: ", data)
                # print("received correct START")
                # only accepted payload for START is zero
                return data == 0
        except Exception as e:
            print("WHAAAAT ", e)
            traceback.print_exc()
            client_log.log(config.LogLevels.ERROR.value, "Timed out: {}".format(e))


    def send_pos(self, data):
        try:
            pkt = packet.make_pkt(config.MsgTypes.POS.value, data)

            self.client.send(pkt)
            return self.recv_pos_msg()
            
        except socket.error as e:
            client_log.log(config.LogLevels.ERROR.value, "Error sending {}: {}".format(data, e))

    def get_state(self):
        return self.state

    def close(self):
        self.client.close()
