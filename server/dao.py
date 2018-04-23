#  server DAO

import rethinkdb as r

def connect_database(host, port, db):
    global DB_CONN
    DB_CONN = r.connect(host=host, port=port, db=db)

#
#  TABLE: clients (client/username mapping)
#

def get_username_for_client(clientid):
    result = r.table('clients').get(clientid).run(DB_CONN)
    if result:
        return result['username']
    else:
        return None

def set_username_for_client(clientid, username):
    r.table('clients').insert(
        {'id': clientid, 'username': username}, 
        conflict = 'replace'
    ).run(DB_CONN)

def delete_username_for_client(clientid):
    r.table('clients').get(clientid).delete().run(DB_CONN)

#
#  TABLE: players (in-game player traits/status/possessions)
#

def get_player(username):
    result = r.table('players').get(username).run(DB_CONN)
    return result

def set_player(player):
    r.table('players').insert(
        player, 
        conflict = 'replace'
    ).run(DB_CONN)

def update_player(username, player):
    r.table('players').get(username).update(player).run(DB_CONN)

def delete_player(username):
    r.table('players').get(username).delete().run(DB_CONN)

#
#  TABLE: items (in-game object definitions)
#

#
#  TABLE: locations (in-game location definitions)
#