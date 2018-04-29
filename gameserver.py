#  main server file

import socket
import ssl
import sys
import queue

from server.transport.courier_in import *
from server.transport.courier_out import *
from server.transport.socket_in import recv_socket
from server.transport.socket_out import send_socket

from server.storage.login import LoginDAO
from server.storage.game import GameDAO

from server.game.input import process_typed_input
from server.game.system_commands import system_cmds

import common.messages as messenger

class PymugServer:
    def __init__(self, certfile, keyfile):
        self._cert = certfile
        self._key = keyfile
        self._gamethreads = 5
        self._host = ''
        self._port = 29999
        self._db_host = 'localhost'
        self._db_port = 28015
        self._connbuffer = 5
        self._usercmds = {}
        self._syscmds = system_cmds()
    
    #
    #  server property setters
    #
    
    def set_server_host(self, host):
        if isinstance(host, str):
            self._host = host
    def set_server_port(self, port):
        if isinstance(port, int):
            self._port = port
    def set_db_host(self, host):
        if isinstance(host, str):
            self._db_host = host
    def set_db_port(self, port):
        if isinstance(port, int):
            self._db_port = port
    def set_game_thread_count(self, count):
        if isinstance(count, int):
            self._gamethreads = max(1, count)
    def set_connection_buffer(self, buff_len):
        if isinstance(buff_len, int):
            self._connbuffer = max(0, buff_len)
    
    #
    #  command registration
    #
    
    def register_player_command(self, cmd, gamefunc):
        if isinstance(cmd, str) and callable(gamefunc):
            self._usercmds[cmd] = gamefunc
        else:
            raise ValueError('cmd must be a string, and gamefunc must be a function')
    
    def register_system_command(self, cmd, gamefunc):
        if isinstance(cmd, str) and callable(gamefunc):
            if cmd in self._syscmds:
                self._syscmds[cmd] = gamefunc
            else:
                raise ValueError('"{0}" is not a recognized system command'.format(cmd))
        else:
            raise ValueError('cmd must be a string, and gamefunc must be a function')
    
    #
    #  magick time
    #
    
    def run(self, debug=False):
        #
        #  define queues
        q_courier_in = queue.Queue()
        q_gamethread = queue.Queue()
        q_courier_out = queue.Queue()
        
        #
        #  setup architecture
        logindao = LoginDAO(self._db_host, self._db_port, 'login')
        courier_in = CourierInbound(q_courier_in, q_courier_out, q_gamethread, logindao, messenger)
        courier_out = CourierOutbound(q_courier_out, messenger)
        courier_in.run()
        courier_out.run()
        for _ in range(self._gamethreads):
            start_new_thread(process_typed_input, (q_gamethread, q_courier_out, self._usercmds, self._syscmds, GameDAO(), messenger))
        
        #
        #  connection loop
        sock = socket.socket()
        s = ssl.wrap_socket(sock, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile=self._cert, keyfile=self._key)
        s.bind((self._host, self._port))
        s.listen(self._connbuffer)
        
        print('Server ready!')
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
    if len(sys.argv)<3:
        print('must provide public cert and key files on command line to run gameserver.py directly')
        exit()
    server = PymugServer(sys.argv[1], sys.argv[2])
    server.run()