#  main client file

import socket
import ssl
import sys
import queue
import time

from transport.socket_in import recv_socket
from transport.socket_out import send_socket

host = 'localhost'
port = 29999

sock = socket.socket()
s = ssl.wrap_socket(sock, server_side=False, ssl_version=ssl.PROTOCOL_TLSv1_2)

s.connect((host, port))

while True:
    line = input().strip()
    if line == 'exit':
        break
    s.send(bytes(len(line).to_bytes(2, 'big')+bytes([ord(x) for x in line])))
    time.sleep(1)
    resp = s.recv(1024)
    print(str(resp[2:], encoding='utf-8'))
s.close()



"""
for i in range(65,75):
    s.send(bytes([0,1,i]))
    time.sleep(1)
s.close()
"""