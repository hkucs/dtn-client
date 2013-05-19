import socket
import utils

from config import *

if __name__ == '__main__':
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.6.1.101', int(GATEWAY_DAT_PORT)))
    data = 'Hello, world!'
    s.sendall(data)
    result = s.recv(BUFFER_LEN)
    print result
    s.close()
    '''
    utils.send_file("10.6.1.101", int(GATEWAY_DAT_PORT), "12345678_0002", BUFFER_LEN)
