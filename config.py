""" Use python 3.7.2 64 bit on Mac OSX + pygame 1.9.2 
    SDL issue: https://bugzilla.libsdl.org/show_bug.cgi?id=4272
"""

from enum import Enum

SERVER_IP = "127.0.0.1"
PORT = 60000

# 2 bytes message type +
# 4 bytes float / int +
# 4 bytes float / int
BUFF_SIZE = 10

""" Window """
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
WINDOW_MARGIN = 20

""" Paddle """
PADDLE_SIZE = [10,140]
PADDLE_SPEED = 8

""" Ball DO NEED THAT """
BALL_SIZE = 10



""" Network """
class MsgTypes(Enum):
    PADDLE_POS = 1
    BALL_POS = 2
    WAIT = 3
    SCORE = 4
    START = 5
    STATE = 6

""" Log """
class LogLevels(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3