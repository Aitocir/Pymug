#  Pymug client

import socket
import ssl
import sys
import queue
import time
from _thread import start_new_thread

from client.transport.socket_in import recv_socket
from client.transport.socket_out import send_socket
from client.transport import courier

from client import gameview

import common.messages as messenger

host = sys.argv[1] if len(sys.argv)>1 else 'localhost'
port = int(sys.argv[2]) if len(sys.argv)>2 else 29999

sock = socket.socket()
s = ssl.wrap_socket(sock, server_side=False, ssl_version=ssl.PROTOCOL_TLSv1_2)
s.connect((host, port))

qrecv = queue.Queue()
qsend = queue.Queue()
start_new_thread(recv_socket, (s, qrecv,))
start_new_thread(send_socket, (s, qsend,))

qprint = queue.Queue()
qscan = queue.Queue()

start_new_thread(courier.process_requests, (qscan, qsend, messenger,))
start_new_thread(courier.process_responses, (qrecv, qprint, messenger,))

gameview.start(qscan, qprint, 'Pymug Client')
