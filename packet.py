from config import *
import logging
from struct import *

def make_pkt(msg_type, data):
    if msg_type == MsgTypes.POS.value:
        """ data is location type [x,y] """
        return pack("Hff", msg_type, data[0], data[1])
    elif msg_type == MsgTypes.WAIT.value:
        return pack("HH", msg_type, 0x0)
    else:
        logging.warning("make_pkt: Dont know the type of message")

    
def unmake_pkt(msg_type,  data):
    if msg_type == MsgTypes.POS.value:
        """ data is location type [x,y] """
        msg = unpack("Hff", data)

        return [msg[1], msg[2]] # x and y
    elif msg_type == MsgTypes.WAIT.value:
        flag = unpack("HH", msg_type, 0x0)

    else:
        logging.warning("unmake_pkt: Dont know the type of message")
