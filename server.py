#!/usr/bin/env python

import datetime
import unittest
import os
import sys
import socket
import asyncore
import asynchat
import threading
import errno
import time
import atexit
import warnings
import optparse
import json

from config import *
from utils import *

class RepeatedTimer:

    def __init__(self, timeout, fun):
        self.timeout = timeout
        self.fun = fun

    def start(self):
        def main():
            self.fun()
            self.start()
        self.timer = threading.Timer(1, main)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

class Handler(asynchat.async_chat):
    ac_in_buffer_size = BUFFER_LEN
    ac_out_buffer_size = BUFFER_LEN

    def __init__(self, conn):
        asynchat.async_chat.__init__(self, conn)
        self.in_buffer = []
        self.closed = False
        #self.push(b("220 Ready\r\n"))

    def handle_read(self):
        data = self.recv(BUFFER_LEN)
        #print "in_buffer len: %s" % len(self.in_buffer)
        self.in_buffer.append(data)

    def get_data(self):
        return b('').join(self.in_buffer)

    def handle_close(self):
        print "Buffer length: %s" % len(self.in_buffer)
        # assume the chunk can fit in RAM
        #ts = datetime.datetime.now().isoformat()
        job_id = self.in_buffer[0]
        chunk_id = self.in_buffer[1]
        self.f = open('%s_%s' % job_id,chunk_id, 'wb')
        for c in self.in_buffer[2:]:
            self.f.write(c)
        self.f.close()
        self.close()
        # critical, write to cache table
        add_job_chunk(job_id, chunk_id)

    def close(self):
        asynchat.async_chat.close(self)
        self.closed = True

    def handle_error(self):
        raise

class ListenHandler(asynchat.async_chat):

    def __init__(self, conn):
        asynchat.async_chat.__init__(self, conn)
        self.set_terminator('EOF\n')
        self.in_buffer = []
        self.closed = False

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.in_buffer.append(data)
        # parse the json message
        decoded_json = json.loads(data)
        print 'Decoded json:'
        print decoded_json

        # is it a response?
        # accept_or_not?
        # right now, assume all jobs are accepted.


        # is it a transmit command?
        # initial implementation: send directly from this class
        if 'next_hop' in decoded_json:
            # send file
            next_hop = str(decoded_json.get('next_hop'))
            filename = str(decoded_json.get('job_id')) + str(decoded_json.get('chunk_id'))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((next_hop, int(GATEWAY_DAT_PORT)))
            f = open(filename, 'rb')
            # job_id and chunk_id padding
            s.send(str(decoded_json.get('job_id')))
            s.send(str(decoded_json.get('chunk_id')))

            while True:
                chunk = f.read(BUFFER_LEN)
                if not trunk:
                    break
                s.sendall(chunk)
            s.close()
            f.close()


    def get_log(self):
        if len(self.in_buffer):
            print 'Received %s commands' % len(self.in_buffer)
            for x in self.in_buffer:
                print x

    def close(self):
        asynchat.async_chat.close(self)
        self.closed = True

    def handle_error(self):
        raise


class Server(asyncore.dispatcher, threading.Thread):

    handler = Handler

    def __init__(self, address):
        threading.Thread.__init__(self)
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(10)
        self.host, self.port = self.socket.getsockname()[:2]
        print self.host, self.port
        self.handler_instance = None
        self._active = False
        self._active_lock = threading.Lock()

    # --- public APIs

    @property
    def running(self):
        return self._active

    def start(self):
        assert not self.running
        self.__flag = threading.Event()
        threading.Thread.start(self)
        self.__flag.wait()

    def stop(self):
        assert self.running
        self._active = False
        self.join()
        assert not asyncore.socket_map, asyncore.socket_map

    def wait(self):
        # wait for handler connection to be closed, then stop the server
        while not getattr(self.handler_instance, "closed", True):
            time.sleep(0.01)
        self.stop()

    # --- internal APIs

    def run(self):
        self._active = True
        self.__flag.set()
        while self._active and asyncore.socket_map:
            self._active_lock.acquire()
            asyncore.loop(timeout=0.01, count=1)
            self._active_lock.release()
        asyncore.close_all()

    def handle_accept(self):
        conn, addr = self.accept()
        self.handler_instance = self.handler(conn)

    def handle_connect(self):
        self.close()
    handle_read = handle_connect

    def writable(self):
        return 0

    def handle_error(self):
        raise

class ListenServer(asyncore.dispatcher, threading.Thread):

    handler = ListenHandler

    def __init__(self, address):
        threading.Thread.__init__(self)
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(4)
        self.host, self.port = self.socket.getsockname()[:2]
        self.handler_instance = None
        self._active = False
        self._active_lock = threading.Lock()

    # --- public APIs

    @property
    def running(self):
        return self._active

    def start(self):
        assert not self.running
        self.__flag = threading.Event()
        threading.Thread.start(self)
        self.__flag.wait()

    def stop(self):
        assert self.running
        self._active = False
        self.join()
        assert not asyncore.socket_map, asyncore.socket_map

    def wait(self):
        # wait for handler connection to be closed, then stop the server
        while not getattr(self.handler_instance, "closed", True):
            time.sleep(0.01)
        self.stop()


    # --- internal APIs

    def run(self):
        self._active = True
        self.__flag.set()
        while self._active and asyncore.socket_map:
            self._active_lock.acquire()
            asyncore.loop(timeout=0.01, count=1)
            self._active_lock.release()
        asyncore.close_all()

    def handle_accept(self):
        conn, addr = self.accept()
        self.handler_instance = self.handler(conn)

    def handle_connect(self):
        self.close()

    handle_read = handle_connect

    def writable(self):
        return 0

    def handle_error(self):
        raise
