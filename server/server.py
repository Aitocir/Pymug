#  main server file

import queue

from postoffice import PostOffice
import dao


def process_client_message(inbox, dao):
    while True:
        while not inbox.empty():
            client_addr, message = inbox.get()
            #  check db for client_addr
            username = dao.get_username_for_client(client_addr)
            if username:
                #  TODO: process message for logged in user
            else:
                #  TODO: try to use message as validation (only message we care about from unknown clients)

def start():
    po = PostOffice(port=29999, host='', backlog=5)
    inbox = queue.Queue()
    po.run(inbox, debug=True)