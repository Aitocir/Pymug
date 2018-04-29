
def process_game_input(q, q_output, player_commands, system_commands, db):
    while True:
        task = q.get()
        #
        #  user input
        if task[0] == 0:
            username = task[1]
            terms = task[2].split()
            if terms[0] in player_commands:
                output_messages = player_commands[terms[0]](username, db, terms)
                for m in output_messages:
                    q_output.put((0, m[0], bytes(m[1], encoding='utf-8')))
            else:
                q_output.put((0, username, bytes('Unknown command: "{0}"'.format(terms[0]), encoding='utf-8')))
        #
        #  automated input
        elif task[0] == 1:
            if task[2] in system_commands:
                output_messages = system_commands[task[2]](task[1], db)
                for m in output_messages:
                    q_output.put((0, m[0], bytes(m[1], encoding='utf-8')))