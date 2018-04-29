#  object used to process outgoing socket traffic

from _thread import start_new_thread

class CourierOutbound:
    def __init__(self, q_outbound):
        self._q = q_outbound
        self._clients = {}
        self._sq = {}
    def _loop(self):
        while True:
            task = self._q.get()
            if task[0] == 0:     #  traffic going to a socket
                if task[1] in self._sq:
                    self._sq[task[1]].put(task[2])
                elif task[1] in self._clients and self._clients[task[1]] in self._sq:
                    self._sq[self._clients[task[1]]].put(task[2])
            elif task[0] == 1:   #  new address/socketQ 
                self._sq[task[1]] = task[2]
            elif task[0] == 2:   #  new clientid/username mapping
                self._clients[task[1]] = task[2]
                print('mapped {0} to {1}'.format(task[1], task[2]))
            elif task[0] == -1:  #  inbound socket closed
                #  self._sq.pop()
                self._clients.pop(task[1], None)
    def run(self):
        start_new_thread(self._loop, tuple())