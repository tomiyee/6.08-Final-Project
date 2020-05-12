import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def room_code_check(request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns the string "false" if no room, and the string "true"
    """

    if 'room_code' not in request['values']:
        return "Misssing Room Code"
    room_code = request['values']['room_code'].strip()

    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    conn.commit() # commit commands
    conn.close() # close connection to database

    response = "false"
    if len(room_rows) > 0:
        response = "true"

    return response

def in_lobby(request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns the string "false" if not in_lobby, and the string "true" if in_lobby
    """

    if 'room_code' not in request['values']:
        return 'Missing room_code'
    room_code = request['values']['room_code']

    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    conn.commit() # commit commands
    conn.close() # close connection to database

    if len(room_rows) == 0:
        return "Room code does not exist."

    room_data = json.loads(room_rows[0][0])

    if room_data["game_data"]["in_lobby"]:
        return "true"
    return "false"
