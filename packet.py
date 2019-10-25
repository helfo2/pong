from config import *
import logging
import struct

def make_pkt(msg_type, data):
    if msg_type == MsgTypes.POS.value:
        """ data is location type [x,y] """
        return struct.pack("Hff", msg_type, data[0], data[1])
    else:
        logging.warning("make_pkt: Dont know the type of message")

    
def unmake_pkt(msg_type, pkt):
    if msg_type == MsgTypes.POS.value:
        """ data is location type [x,y] """
        msg = struct.unpack("Hff", pkt)

        return [msg[1], msg[2]] # x and y
    else:
        logging.warning("unmake_pkt: Dont know the type of message")
