from enum import Enum

LOCALHOST = "127.0.0.1"
PORT = 1235

BUFF_SIZE = 2048

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
PADDLE_SIZE = [15,200]
PADDLE_SPEED = 8

""" Network """
class MsgTypes(Enum):
    POS = 1