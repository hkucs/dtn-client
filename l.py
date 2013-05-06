
'''
src: https://gist.github.com/micktwomey/606178
'''
import multiprocessing
import socket
import utils

from config import *

def handle(conn, addr):
    import logging,json
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process: %r" % (addr,))
    try:
        logger.debug("Connected %r at %r", conn, addr)
        data = conn.recv(BUFFER_LEN)
        decoded_json = json.loads(data)
        print decoded_json

        if 'next_hop' in decoded_json:
            next_hop = str(decoded_json.get('next_hop'))
            job_id = str(decoded_json.get('job_id')).zfill(8)
            chunk_id = str(decoded_json.get('chunk_id')).zfill(4)
            filename = '/data/%s_%s' % (job_id, chunk_id)
            # send file
            utils.send_file(next_hop, int(GATEWAY_DAT_PORT), filename, BUFFER_LEN)

    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        conn.close()

class Listener(object):
    def __init__(self, hostname, port):
        import logging
        self.logger = logging.getLogger("Listener")
        self.hostname = hostname
        self.port = port

    def start(self):
        self.logger.debug("listening to commands")
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
    logging.basicConfig(level=logging.DEBUG)
    listener = Listener("0.0.0.0", int(GATEWAY_CMD_PORT))

    try:
        logging.info("Listening")
        listener.start()
    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
    logging.info("All done")
