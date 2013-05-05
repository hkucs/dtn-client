#!/usr/bin/env python


import unittest
import os,sys,socket,time,json

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config import *
from server import Server,ListenServer


'''
Make sure SimpleController.py is up before the test
'''
class TestSimpleController(unittest.TestCase):
    def setUp(self):
        self.client = socket.socket()
        self.client.connect(('127.0.0.1', 8088))

    def tearDown(self):
        self.client.close()

    def test_connect_controller(self):

        start_time = '2013-05-05-17-33-33'
        end_time = '2013-05-05-17-59-50'
        size = '1000'
        source = '10.6.0.102'
        destination = '10.6.0.101'
        type_ = 'Undefined'
        cmd = {'start_time': start_time, 'end_time': end_time, 'size': size, 'source': source, 'destination': destination, 'type': type_}
        cmd_json = json.dumps(cmd)

        self.client.send(cmd_json)

'''
To make sure that the server can receive chunks correctly
'''
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

class TestListener(unittest.TestCase):

    def setUp(self):
        # server
        self.listenserver = ListenServer(('127.0.0.1', int(GATEWAY_CMD_PORT)))
        self.listenserver.start()

        # client
        self.client = socket.socket()
        self.client.connect((self.listenserver.host, self.listenserver.port))
        self.client.settimeout(10)

    def tearDown(self):
        self.client.close()
        if self.listenserver.running:
            self.listenserver.stop()
        self.listenserver = None  # garbage collection

    def test_listener(self):
        commands = ['LIST', 'GET', 'POST']
        for x in commands:
            print x
            self.client.sendall(x)
            time.sleep(0.01)
        self.client.close()
        self.listenserver.wait()
        log = self.listenserver.handler_instance.get_log()

class TestListenerJson(TestListener):

    def test_listener(self):
        start_time = '2013-05-05-17-33-33'
        end_time = '2013-05-05-17-59-50'
        size = '1000'
        source = '10.6.0.102'
        destination = '10.6.0.101'
        type_ = 'Undefined'
        cmd = {'start_time': start_time, 'end_time': end_time, 'size': size, 'source': source, 'destination': destination, 'type': type_}
        cmd_json = json.dumps(cmd)
        self.client.send(cmd_json)

        self.client.close()
        self.listenserver.wait()
        log = self.listenserver.handler_instance.get_log()


def test_main():
    print 'test main'

    test_suite = unittest.TestSuite()
    #test_suite.addTest(unittest.makeSuite(TestSendfile))
    #test_suite.addTest(unittest.makeSuite(TestListenerJson))
    test_suite.addTest(unittest.makeSuite(TestSimpleController))
    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == '__main__':
    test_main()
