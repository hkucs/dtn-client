#!/usr/bin/env python
'''
src: https://gist.github.com/micktwomey/606178
'''
import multiprocessing
import socket
import logging

from config import *

logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S')

def handle(conn, addr):
    logger = logging.getLogger("TransHdlr: %r" % (addr,))
    try:
        logger.debug("Connected %r at %r", conn, addr)
        data = conn.recv(HEADER_LEN)
        job_id = data[0:8]
        chunk_id = data[9:13]
        logger.debug('Transmitting Job %s, Chunk %s', job_id, chunk_id)
        filename = data
        f = open('/data/%s' % filename, "wb")
        while True:
            data = conn.recv(BUFFER_LEN)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            f.write(data)
            #logger.debug("Received data %r", data)
            #conn.sendall(data)
            #logger.debug("Sent data")

    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        conn.close()

def hdlr_counter():
    logger = logging.getLogger("Counter")
    while True:
        print multiprocessing.active_children()
        time.sleep(5)

class Server(object):
    def __init__(self, hostname, port):
        self.logger = logging.getLogger("Server")
        self.hostname = hostname
        self.port = port

    def start(self):
        self.logger.debug("Listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        # new thread for counting the number of threads within interval
        counter = multiprocessing.Process(target=hdlr_counter)
        process.daemon = True
        process.start()

        while True:
            conn, addr = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn,addr))
            print multiprocessing.active_children()
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

if __name__ == "__main__":

    server = Server("0.0.0.0", int(GATEWAY_DAT_PORT))

    try:
        logging.info("Listening")
        server.start()
    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
    logging.info("All done")
