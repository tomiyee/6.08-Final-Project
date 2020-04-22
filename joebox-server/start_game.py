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
    pass
