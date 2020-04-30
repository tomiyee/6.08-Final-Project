import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def waiting_for_submissions (request):
    """
    Given the GET request with:
      String room_code - The characters that represent the room code

    This API call should access the room data for the room_code, and check if
    the value for "game_data", under "waiting_for_submissions" is True. If
    waiting_for_votes is True, then this API call should return "true", and
    "false" otherwise.

    Returns "true" if the game is waiting for submissions, and "false" otherwise
    """

    if 'room_code' not in request['values']:
        return "Misssing Room Code"
    room_code = request['values']['room_code']

    # Read the Room Data
    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    conn.commit()
    conn.close()

    if len(room_rows) == 0:
        return "No room with room code: " + room_code

    room_data = json.loads(room_rows[0][0])
    
    # Temporary Return Value
    return "true" if room_data['game_data']['waiting_for_submissions'] else "false"
