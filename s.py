
'''
src: https://gist.github.com/micktwomey/606178
'''
import multiprocessing
import socket

from config import *

def handle(conn, addr):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process: %r" % (addr,))
    try:
        logger.debug("Connected %r at %r", conn, addr)
        data = conn.recv(HEADER_LEN)
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
    def __init__(self, hostname, port):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port

    def start(self):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, addr = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn,addr))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S')
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
