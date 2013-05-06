import socket

from config import *

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.6.1.101', int(GATEWAY_DAT_PORT)))
    data = 'Hello, world!'
    s.sendall(data)
    result = s.recv(1024)
    print result
    s.close()
