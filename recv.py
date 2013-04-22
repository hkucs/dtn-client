from config import *
import socket,sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("localhost", int(GATEWAY_DAT_PORT)))
s.listen(10)
file_count = 0

while True:
    sc,address = s.accept()
    print 'Connected by',address
    f = open('file_recv'+str(file_count), 'wb')
    file_count = file_count + 1
    while True:
        data = sc.recv(1024)
        if not data:
            break
        f.write(data)
    f.close()

    sc.close()
    print 'Disconnected.'

s.close()

