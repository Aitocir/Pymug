#  main server file

import socket
import ssl
import sys
import queue

from transport.courier_in import *
from transport.courier_out import *
from transport.socket_in import recv_socket
from transport.socket_out import send_socket

from storage.login import LoginDAO
#from storage.game import GameDAO

from game.input_processor import process_game_input


def run(certfile, keyfile, game_thread_count=5, host='', port=29999, db_host='localhost', db_port=28015, conn_buffer=5, debug=False):
    #  define queues
    q_courier_in = queue.Queue()
    q_gamethread = queue.Queue()
    q_courier_out = queue.Queue()
    #  setup architecture
    logindao = LoginDAO(db_host, db_port, 'login')
    courier_in = CourierInbound(q_courier_in, q_courier_out, q_gamethread, logindao)
    courier_out = CourierOutbound(q_courier_out)
    courier_in.run()
    courier_out.run()
    for _ in range(game_thread_count):
        start_new_thread(process_game_input, (q_gamethread,))
    #  connection loop
    sock = socket.socket()
    s = ssl.wrap_socket(sock, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile=certfile, keyfile=keyfile)
    s.bind((host, port))
    s.listen(conn_buffer)
    while True:
        conn, addr = s.accept()
        address = '__'.join([str(x) for x in addr])
        if debug:
            print('Got connection from: {0}'.format(address))
        q_socket_out = queue.Queue()
        start_new_thread(recv_socket, (conn, q_courier_in, address,))
        start_new_thread(send_socket, (conn, q_socket_out,))
        q_courier_in.put((1, address))
        q_courier_out.put((1, address, q_socket_out))
    

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])