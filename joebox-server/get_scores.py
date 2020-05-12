import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def get_scores (request):
    """
    Given the GET request with:
      String room_code - The characters that represent the room code

    This call should loop through all the player data and return a comma -
    separated string, where every even-number item is the player name, and every
    odd-number item is the score of the player that precedes it. For example, if
    "Player1" had a score of 100, and "Player2" had a score of 200, then the
    return value should be "Player1,100,Player2,200". The order of the players
    does not matter.

    Returns a comma-separated string of players and their scores
    """

    if 'room_code' not in request['values']:
        return "Misssing Room Code"
    room_code = request['values']['room_code'].strip()


    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    conn.commit()
    conn.close()

    if len(room_rows) == 0:
        return "No room with room code: " + room_code

    if len(room_rows) > 1:
        return "More than one room with this room code"

    #dictionary of game and player data for room with given room code
    room_data = json.loads(room_rows[0][0])
    #list of players currently in game
    data = []
    for player in room_data['player_data']:
        data.append(player)
        data.append(str(room_data['player_data'][player]['score']))

    # Joins the list of strings with commas in between.
    return ",".join(data)
