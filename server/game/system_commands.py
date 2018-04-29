#  system command definitions
#  all functions should return lists of (username, message) tuples

def _init(username, db, messenger):
    #  TODO: create all needed documents in db for brand new user with initial values
    return []

def _login(username, db, messenger):
    #  This event is triggered when a player logs in
    #  convenient signal for sending welcome messages, server announcements, etc.
    return [messenger.plain_text('Welcome to this generic pymug server, {0}!'.format(username), username)]

def system_cmds():
    return {
        'registered': _init,
        'logged-in': _login,
    }