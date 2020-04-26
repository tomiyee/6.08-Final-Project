import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def list_players (request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns a comma-separated string of players in the specified room
    """

    players = []

    if 'room_code' not in request['values']:
        return "Missing Room Code"
    room_code = request['values']['room_code']


    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    conn.commit()
    conn.close()

    if len(room_rows) == 0:
        return "No room with room code: " + room_code

    if len(room_roms) > 1:
        return "More than one room with this room code"

    #dictionary of game and player data for room with given room code
    room_data = json.loads(room_rows[0][0])
    #list of players currently in game
    players = [player for player in room_data['player_data']:

    if len(players) == 0:
        return "No players in game currently"

    # Joins the list of strings with commas in between.
    return ",".join(players)
