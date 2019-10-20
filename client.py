import socket
import logging
import threading

pongClient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
pongClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
pongClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


def main():
    pass

if __name__ == "__main__":
    main()