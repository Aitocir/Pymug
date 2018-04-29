#  object used to process incoming socket traffic

from _thread import start_new_thread

class CourierInbound:
    def __init__(self, q_inbound, q_courier_out, q_game, userdb):
        self._q = q_inbound
        self._qout = q_courier_out
        self._qgame = q_game
        self._users = {}
        self._db = userdb
    def _build_message(self, cid, text):
        return (0, cid, bytes(text, encoding='utf-8'))
    def _build_client_mapping(self, username, cid):
        return (2, username, cid)
    def _build_player_signal(self, username, text):
        return (0, username, text)
    def _build_system_signal(self, username, type):
        return (1, username, type)
    def _parse_anon_payload(self, payload):
        payloadstr = str(payload, encoding='utf-8')
        form = payloadstr.split()
        if len(form) == 3 and form[0] == 'login':
            return {'type':form[0], 'username':form[1], 'password':form[2]}
        elif len(form) == 4 and form[0] == 'register':
            return {'type':form[0], 'username':form[1], 'password':form[2], 'email':form[3]}
        else:
            return None
    def _parse_loggedin_payload(self, payload):
        return str(payload, encoding='utf-8')
    def _validate_registration(self, username, password, email):
        #  TODO: actual validation of any kind
        uvalid = True
        pvalid = True
        evalid = '@' in email
        return uvalid and pvalid and evalid
    def _loop(self):
        while True:
            task = self._q.get()
            print(task)
            if task[0] == 0:    #  traffic from a socket
                cid = task[1]
                payload = task[2]
                #
                #  not logged in
                if not self._users[cid]:
                    form = self._parse_anon_payload(payload)
                    if not form:
                        self._qout.put(self._build_message(cid, 'login <username> <password>\nregister <username> <password> <email>'))
                    elif form['type'] == 'login':
                        if self._db.check_login(form['username'], form['password']):
                            self._users[cid] = form['username']
                            self._qout.put(self._build_client_mapping(form['username'], cid))
                            #  TODO: remove below call and send the client additional info such as last login time via system signal
                            self._qout.put(self._build_message(cid, 'Welcome back, {0}!'.format(form['username'])))
                            self._qgame.put(self._build_system_signal(form['username'], 'logged-in'))
                        else:
                            self._qout.put(self._build_message(cid, 'Wrong username or password'))
                    elif form['type'] == 'register':
                        if self._validate_registration(form['username'], form['password'], form['email']):
                            if self._db.save_registration(form['username'], form['password'], form['email']):
                                self._qgame.put(self._build_system_signal(form['username'], 'registered'))
                                #  TODO: remove this once the system signal generates this message
                                self._qout.put(self._build_message(cid, 'Successfully registered {0}! Now try logging in'.format(form['username'])))
                            else:
                                self._qout.put(self._build_message(cid, 'Username {0} already exists; try logging in.'.format(form['username'])))
                        else:
                            self._qout.put(self._build_message(cid, 'bad values provided for registration form (is your email valid?)'))
                #
                #  logged in
                else:
                    text = self._parse_loggedin_payload(payload)
                    self._qgame.put(self._build_player_signal(self._users[cid], text))
            elif task[0] == 1:  #  new address
                cid = task[1]
                self._users[cid] = None
            elif task[0] == -1: #  closed socket
                self._users.pop(task[1])
                self._qout.put(task)
                print('socket closed: {0}'.format(task[1]))
    def run(self):
        start_new_thread(self._loop, tuple())