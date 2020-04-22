import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def start_game (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code

    Returns a string, representing all usernames separated by ","
    """

    if 'room_code' not in request['form']:
        return "Misssing Room Code"

    room_code = request['form']['room_code']

    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()

    if len(room_rows) > 0:
        conn.commit() # commit commands
        conn.close() # close connection to database
        return "Room does not exist"

    room_data = json.loads(room_rows[0][0])

    if room_data['game_data']['in_lobby'] == False:
        conn.commit() # commit commands
        conn.close() # close connection to database
        return "Game already in progress"

    room_data['game_data']['in_lobby'] = False

    # (TODO) Trigger events that occur once the game starts, like setting the question


    new_room_json = json.dumps(room_data)
    connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code))
    conn.commit() # commit commands
    conn.close() # close connection to database

    # Constructs a list of player names separated by commas
    players = ",".join([player for player in room_data['player_data']])
    return players
