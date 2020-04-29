import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def dump_data (request):
    """
    Given the GET request:
        (Opt) String room_code - The characters that rep the room code

    Returns a huge json string representing an array containing [room_code, room_data]
    pairs if not given a specific room code
    For example
        [ ["ABCD", {...}],
          ["EFGH", {...}],
          ["IJKL", {...}] ]

    Returns a json string representing the dictionary with the room data
    For example:
        {...}
    """

    # Gets only the one item
    if 'room_code' in request['values']:
        conn = sqlite3.connect(bluffalo_db)
        connection = conn.cursor()
        room_data = connection.execute('''SELECT game_data FROM game_table WHERE room_code=?''', (request['values']['room_code'],)).fetchall();
        conn.commit()
        conn.close()
        if len(room_data) == 0:
            return '"Room Code does not exist"'
        return room_data[0][0]

    # dumps all data
    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()
    all_data = connection.execute('''SELECT * FROM game_table''').fetchall();
    conn.commit()
    conn.close()

    # Generates a list of [room_code, room_data] pairs
    all_data = [[row[0], json.loads(row[1])] for row in all_data]
    return json.dumps(all_data)
