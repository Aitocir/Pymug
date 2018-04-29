import rethinkdb as r
import sys

if __name__ == '__main__':
    #
    #  parameters
    db_host = sys.argv[1]
    db_port = sys.argv[2]
    
    #
    #  init database 
    #  (don't forget to have this running already!)
    conn = r.connect(host=db_host, port=db_port)
    r.db_create('login').run(conn)
    r.db('login').table_create('registrations', primary_key='username').run(conn)
    conn.close()