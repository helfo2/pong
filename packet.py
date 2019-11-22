import config
import logging
import struct

def make_pkt(msg_type, data):
    if msg_type == config.MsgTypes.POS.value:
        """ data is location type [x,y] """

        print("packet made: ", msg_type, data[0], data[1])
        return struct.pack("!Hff", msg_type, data[0], data[1])

    elif msg_type == config.MsgTypes.SCORE.value:
        return struct.pack("!HII", msg_type, data[0], data[1])

    else:
        logging.error("make_pkt: Don't know the type of message")

    

def msg_size_from_type(msg_type):
    if msg_type == config.MsgTypes.POS.value:
        return 8



def solve_msg_type(data):
    """ works with bytes to retrieve msg_type and payload of message """

    print("all data ", data)

    msg_type = data[:2]
    payload = data[2:10]

    return struct.unpack("!H", msg_type)[0], payload


def unmake_pkt(data):
    msg_type, payload = solve_msg_type(data)

    print("msg type is ", str(msg_type))
    print("payload len is ", str(len(payload)))

    if msg_type == config.MsgTypes.POS.value:
        """ data is location type [x,y] """
        msg = struct.unpack("!ff", payload)

        print("msg is ", str(msg))

        return [msg[0], msg[1]] # x and y

    elif msg_type == config.MsgTypes.SCORE.value:
        msg = struct.unpack("!II", payload)

        return [msg[0], msg[1]] # left score and right score

    else:
        logging.error("unmake_pkt: Don't know the type of message")
