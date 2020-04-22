import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def create_room (request):
    """
    Given the POST request with no required parameters:

    Generates a json with no players yet. It is initialized to have no players.

    Returns the room code, made of 4 capital letters (e.g. ABCD)
    """

    new_room = {
      "player_data": {},
      "game_data": {
        "in_lobby": True,
        "current_word": None,
        "current_meaning": None,
        "current_answer": None,
        "round_number": 1,
        "question_number": 1,
        "waiting_for_submissions": False,
        "selecting_options": False
      }
    }

    # insert the new_room to the room_code
    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)
    connection.execute('''CREATE TABLE IF NOT EXISTS game_table (room_code text, game_data text);''') # run a CREATE TABLE command

    # Constantly generates a random room code until there is not a collision
    while True:
        # Generate a random room code
        room_code = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(4)])
        room_data_text = json.dumps(new_room)
        rows = connection.execute('''SELECT * FROM game_table WHERE room_code=?;''', (room_code,)).fetchall()
        if len(rows) > 0:
            continue
        # If no room has this room code, we can stop looping
        break
    # Creates the row with the room code and the empty data
    connection.execute('''INSERT into game_table VALUES (?,?);''', (room_code, room_data_text))
    conn.commit()
    conn.close()
    return room_code
