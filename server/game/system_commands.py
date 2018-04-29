#  system command definitions
#  all functions should return lists of (username, message) tuples

def _init(username, db):
    #  TODO: create all needed documents in db for brand new user with initial values
    return []

def _login(username, db):
    #  TODO: update player status to Active (online)
    #  TODO: return any greeting to be sent to player upon logging in
    return []

def system_cmds():
    return {
        'registered': _init,
        'logged-in': _login,
    }