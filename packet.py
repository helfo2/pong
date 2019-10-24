from config import *
import logging
import struct

class Packet:
    @staticmethod
    def make_pkt(self, msg_type, data):
        if msg_type == MsgTypes.POS.value:
            """ data is location type [x,y] """
            return struct.pack("Hii", msg_type, data[0], data[1])
        else:
            logging.warning("make_pkt: Dont know the type of message")

    @staticmethod
    def unmake_pkt(self, msg_type, pkt):
        if msg_type == MsgTypes.POS.value:
            """ data is location type [x,y] """
            msg = struct.unpack("Hii", pkt)

            return msg[1], msg[2] # x and y
        else:
            logging.warning("unmake_pkt: Dont know the type of message")
