# Distributed Pong
Implementation of a distributed pong game.

This project was created to challenge ourselves into better understanding networks, latency, collision and game development logic. It uses purely sockets in Python 3.8 along with Pygame 1.9.2 to draw objects on the screen surface.

The idea is to keep all network logic simple, by exchanging only one type of packet, called "POS", for position packet. This message contains two floats X and Y plus the message type itself (a small int), totalizing 12 bytes. The server runs on top of TCP, which can add a latency in separated and distant networks due to the overhead of the 40 bytes header. The following diagram illustrates some more about the design of the system.

## Usage
To use it, one should install Python 3.7+ and Pygame 1.9+ on the machine*, then run the server.py and two client.py instances. The config.py file should be saved on both client and server machines and contains some configuration parameters, such as the server host and port, so you probably should take a look at it.


Feel free to use the code and enjoy playing!

*Note that MACOSX systems may have an issue with SDL (on top of which pygame is developed). Make sure to use Python 3.7.2 and Pygame 1.9.2, because for newer versions this could make the screen blank - https://github.com/pygame/pygame/issues/555)
