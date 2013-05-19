from config import *
import socket,sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost", int(GATEWAY_DAT_PORT)))
f=open("10MB2", "rb")

while True:
    chunk = f.read(1024)
    if not chunk:
        break #EOF
    s.sendall(chunk)
s.close()
f.close()
