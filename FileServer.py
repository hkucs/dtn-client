#!/usr/bin/env python
import multiprocessing
import socket
import logging
import time
import datetime

from config import *

logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S')

def handle(conn, addr):
    '''To handle every request that the Listener receives'''

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

class Server(object):
    '''Main class for listening to requests'''
    def __init__(self, hostname, port):
        self.logger = logging.getLogger("Server")
        self.hostname = hostname
        self.port = port

        self.logger_cnt = logging.getLogger("Counter")
        self.proc_cnt = multiprocessing.Value('i', 0)
        self.intv_cnt = 10

    def hdlr_counter(self):
        while True:
            self.logger_cnt.debug("Number of threads: %d", self.proc_cnt.value)
            time.sleep(self.intv_cnt)

    def start(self):
        self.logger.debug("Listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        # new thread for counting the number of threads within interval
        #counter = multiprocessing.Process(target=self.hdlr_counter)
        #counter.daemon = True
        #counter.start()

        while True:
            conn, addr = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn,addr))
            self.proc_cnt.value = self.proc_cnt.value + 1
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
