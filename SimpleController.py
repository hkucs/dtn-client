#!/usr/bin/env python

import sys
import os
import json
import time
import socket
import datetime
from config import *

TIMEOUT=2
LISTENER_ADDR='10.6.0.101'

class Controller():

    def __init__(self):
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', int(CONTROLLER_PORT)))
        self.s.listen(4)
        '''
        self.runnint = True

    def old_run(self):
        while True:
            self.sc, self.addr = self.s.accept()
            print 'Connected by', self.addr
            cmd_json = self.sc.recv(BUFFER_LEN)
            cmd = json.loads(cmd_json)
            print cmd

            #self.sc.send('3.14')
            response = {'job_id': '13', 'accept_or_not': 'true', 'type': 'response'}
            res2 = '23'
            self.sc.send(res2)

            self.sc.close()
            print 'Disconnected'

        self.s.close()

    def send_json(self, j):
        s = socket.socket()
        s.settimeout(TIMEOUT)
        s.connect((LISTENER_ADDR, int(GATEWAY_CMD_PORT)))
        s.sendall(j)
        s.sendall('\n')
        s.close()

    def send_response(self):
        j = {'job_id': '14', 'accept_or_not': 'true', 'chunk_size': '7', 'utility': '2.0', 'type': 'response'}
        je = json.dumps(j)

        print j

        self.send_json(je)

    def send_transmit(self):
        j = {'job_id': '14', 'chunk_id': '1', 'next_hop': '10.6.0.102', 'type': 'transmit'}
        je = json.dumps(j)
        print j
        self.send_json(je)

    def send_notify_dest(self):
        deadline = (datetime.datetime.now() + datetime.timedelta(seconds=90)).strftime("%Y-%m-%d %H:%M:%S")
        j = {'job_id': '14', 'chunk_size': '7', 'deadline': deadline, 'type': 'notify_dest'}
        je = json.dumps(j)
        print j
        self.send_json(je)

    def send_notify_comp(self):
        j = {'job_id': '14', 'chunk_id': '1', 'type': 'notify_comp'}
        je = json.dumps(j)
        print j
        self.send_json(je)


if __name__ == '__main__':
    c = Controller()
    #c.run()
    c.send_response()
    time.sleep(5)
    c.send_transmit()
    time.sleep(2)
    c.send_notify_dest()
    time.sleep(3)
    c.send_response()
    c.send_notify_comp()
