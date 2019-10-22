"""
PONG server
"""

import socket
import threading
import logging
import config
import sys

logging.basicConfig(
    filename="server.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class PongServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        try:
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.server.bind((self.ip, self.port))
            self.clients = []
            self.server.listen(2)

            logging.info("Initialized PONG server at {}:{}".format(ip, str(port)))
        except socket.error as e:
            logging.error("Socket error while binding: {}".format(e))
            sys.exit(1)

    def send_data(self, data, addr):
        logging.info("Sending {} to {}".format(str(data), addr))

        self.server.sendto("ok".encode(), addr)

    def listen(self):
        run = True
        try:
            while(run):
                conn, addr = self.server.accept()
                threading.Thread(target=self.run_client, args=(conn,))
        except KeyboardInterrupt:
            logging.warning("Interrupted form keyboard")

    def run_client(self, conn):
        reply = ""

        while True:
            try:
                data = conn.recv(config.BUFF_SIZE)
                reply = data.decode("utf-8")

                if not data:
                    logging.info("Client {} disconnected".format(conn))
                else:
                    print("Received: ", reply)
                    logging.info("Received {} from {}".format(str(reply), conn))
                    print("Sending: ", reply)

                conn.send(reply.encode())
            except Exception as e:
                logging.error("Error at run_client(): {}".format(e))
            

def main():
    pongServer = PongServer(config.LOCALHOST, config.PORT)
    pongServer.listen()
    
if __name__ == "__main__":
    main()


