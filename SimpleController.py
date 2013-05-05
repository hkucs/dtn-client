#!/usr/bin/env python

import sys,os,json,time,socket
from config import *

class Controller():

    def init(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', int(CONTROLLER_PORT)))
        self.s.listen(4)

    def run(self):
        while True:
            self.sc, self.addr = self.s.accept()
            print 'Connected by', self.addr
            cmd_json = self.sc.recv(BUFFER_LEN)
            cmd = json.loads(cmd_json)
            print cmd

            self.sc.close()
            print 'Disconnected'

        self.s.close()

if __name__ == '__main__':
    c = Controller()
    c.init()
    c.run()
