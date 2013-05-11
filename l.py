#!/usr/bin/env python
'''
src: https://gist.github.com/micktwomey/606178
'''
import multiprocessing
import threading
import socket
import utils
import os
import shutil
import logging

from config import *

# basic logging config
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%s %m-%d %H:%M:%S')

def handle(conn, addr):
    import json

    #logger = logging.getLogger("Handler: %r" % (addr,))
    logger = logging.getLogger("Handler")

    '''
    # Output logging information to screen
    hdlr_lg_stdout = logging.StreamHandler(sys.stderr)
    logger.addHandler(hdlr_lg_stdout)

    # Output logging information to file
    logfile = 'dtm.log'
    hdlr_lg_file = logging.FileHandler(logfile)
    logger.addHandler(hdlr_lg_file)
    '''

    try:
        #logger.debug("Connected %r at %r", conn, addr)
        data = conn.recv(BUFFER_LEN)
        decoded_json = json.loads(data)
        #print decoded_json
        logger.debug("Raw: %s", decoded_json)

        # get msg type from json
        msg_type = str(decoded_json.get('type'))

        # create file upon successful response
        if msg_type == 'response':
            accept_or_not = str(decoded_json.get('accept_or_not'))
            if accept_or_not == 'true':
                job_id = str(decoded_json.get('job_id')).zfill(8)
                logger.debug("Creating dummy chunks for job #%s", job_id)
                chunk_size = int(decoded_json.get('chunk_size'))

                # create dummy chunks:
                srcfile = '/data/block'
                assert os.path.isabs(srcfile)
                for x in range(0,chunk_size):
                    dstfile = '/data/%s_%s' % (job_id, str(x).zfill(4))
                    shutil.copy(srcfile, dstfile)


        # transmit
        # if 'next_hop' in decoded_json:
        if msg_type == 'transmit':
            next_hop = str(decoded_json.get('next_hop'))
            job_id = str(decoded_json.get('job_id')).zfill(8)
            chunk_id = str(decoded_json.get('chunk_id')).zfill(4)
            filename = '/data/%s_%s' % (job_id, chunk_id)
            # send file
            logger.debug("Sending Job #%s Chunk #%s", job_id, chunk_id)
            utils.send_file(next_hop, int(GATEWAY_DAT_PORT), filename, BUFFER_LEN)

        # notify_dest
        # if 'chunk_size' in decoded_json:
        if msg_type == 'notify_dest':
            logger.debug("Notified by controller: deadline for job.[TODO]")
            d_job_id = str(decoded_json.get('job_id')).zfill(8)
            d_chunk_size = str(decoded_json.get('chunk_size'))
            d_deadline = str(decoded_json.get('deadline'))
            # date str to datetime type.
            #logger.debug("Raw: %s", decoded_json)

        # notify_comp
        if msg_type == 'notify_comp':
            # get job_id and chunk_id
            c_job_id = str(decoded_json.get('job_id')).zfill(8)
            c_chunk_id = str(decoded_json.get('chunk_id')).zfill(4)

            # check whether the cache is on disk
            c_filename = '/data/%s_%s' % (c_job_id, c_chunk_id)
            if os.path.exists(c_filename):
                os.remove(c_filename)



    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        conn.close()

class Listener(object):
    def __init__(self, hostname, port):
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
