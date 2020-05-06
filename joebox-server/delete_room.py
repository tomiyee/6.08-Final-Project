import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def delete_room (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code

    Deletes the row of data from the SQL Database

    Returns if the deletion was "Successful" or if there was "No Room with Room Code:"
    """

    if 'room_code' not in request['form']:
        return "Missing Room Code"

    room_code = request['form']['room_code']

    if delete_room_fn(room_code):
        return "Successful"
    return "No Room with Room Code: {}".format(room_code)

def delete_room_fn (room_code):
    """Enters the bluffalo_db and removes all rows with the given room_code"""
    # insert the new_room to the room_code
    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)
    room_data = connection.execute('''SELECT game_data FROM game_table WHERE room_code=?''', (room_code,)).fetchall();
    connection.execute('''DELETE FROM game_table WHERE room_code =?;''', (room_code,))
    conn.commit()
    conn.close()
    return len(room_data) != 0
