#!/usr/bin/env python


import unittest
import os,sys,socket

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config import *
from server import Server

class TestSendfile(unittest.TestCase):

    def setUp(self):
        # server
        self.server = Server(('127.0.0.1', int(GATEWAY_DAT_PORT)))
        self.server.start()
        # client
        self.client = socket.socket()
        self.client.connect((self.server.host, self.server.port))
        self.client.settimeout(10)

        #self.client.recv(1024)
        self.sockno = self.client.fileno()
        self.file = open('10MB', 'rb')
        self.fileno = self.file.fileno()

    def tearDown(self):
        #save_remove('10MB-1')
        self.file.close()
        self.client.close()
        if self.server.running:
            self.server.stop()
        self.server = None # garbage collection

    def test_send_file(self):
        total_sent = 0
        while True:
            sent = self.file.read(BUFFER_LEN)
            if not sent:
                break #EOF
            self.client.sendall(sent)
        self.client.close()
        self.server.wait()
        data = self.server.handler_instance.get_data()
        print 'Server received: %s' % len(data)
        #time.sleep(20)


def test_main():
    print 'test main'

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSendfile))
    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == '__main__':
    test_main()
