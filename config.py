from enum import Enum

SERVER_IP = "127.0.0.1"
PORT = 1235

BUFF_SIZE = 12

""" Colors """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

""" Window """
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
WINDOW_MARGIN = 20

""" Paddle """
PADDLE_SIZE = [10,140]
PADDLE_SPEED = 8

""" Ball """
BALL_SIZE = 10

""" Initial locations """
PLAYER_1_POS = [WINDOW_MARGIN, WINDOW_HEIGHT/2 - 100]
PLAYER_2_POS = [WINDOW_WIDTH-WINDOW_MARGIN-PADDLE_SIZE[0], WINDOW_HEIGHT/2 - 100]
FLAG_POS = [-1,-1]

""" Network """
class MsgTypes(Enum):
    POS = 1
    PADDLE_POS = 2
    WAIT = 3

""" Log """
class LogLevels(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3