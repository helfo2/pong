import config
import logging
import struct

MSG_TYPE_SIZE = 2
# BUFF_SIZE = 10

def make_pkt(msg_type, data=None):
    if data is None:
        logging.error("make _pkt: No data")

    elif msg_type is config.MsgTypes.WAIT.value:
        return struct.pack("!HI", msg_type, data)

    elif msg_type is config.MsgTypes.START.value:
        return struct.pack("!H", msg_type)

    elif msg_type is config.MsgTypes.POS.value:
        """ data is location type [x,y] """

        print("packet made: ", msg_type, data[0], data[1])
        return struct.pack("!Hff", msg_type, data[0], data[1])

    elif msg_type is config.MsgTypes.SCORE.value:
        return struct.pack("!HII", msg_type, data[0], data[1])

    else:
        logging.error("make_pkt: Don't know the type of message")


def unmake_pkt(data):
    msg_type, payload = solve_msg_type(data)

    print("msg type is ", str(msg_type))
    print("payload len is ", str(len(payload)))

    if msg_type is config.MsgTypes.WAIT.value:
        """ payload is the sleep time in seconds to wait for second player """
        wait_timeout = struct.unpack("!I", payload)
        return wait_timeout

    elif msg_type is config.MsgTypes.START.value:
        """ no payload. 0 wait time to the actual start of the game """
        return 0

    elif msg_type is config.MsgTypes.POS.value:
        """ payload is location type [x,y] """
        msg = struct.unpack("!ff", payload)

        print("msg is ", str(msg))

        return [msg[0], msg[1]] # x and y

    elif msg_type is config.MsgTypes.SCORE.value:
        msg = struct.unpack("!II", payload)

        return [msg[0], msg[1]] # left score and right score

    else:
        logging.error("unmake_pkt: Don't know the type of message")


def solve_msg_type(msg):
    """ works with bytes to retrieve msg_type and payload of message """

    print("whole msg ", msg)

    msg_type, payload = split_msg(msg)

    return struct.unpack("!H", msg_type)[0], payload


def split_msg(data):
    msg_type = data[:MSG_TYPE_SIZE]
    payload = data[MSG_TYPE_SIZE:]

    return msg_type, payload
