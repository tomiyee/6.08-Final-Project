import json
import sqlite3

bluffalo_db = '__HOME__/bluffalo/game_data.db'
# Note json.load(String) and json.dumps(Objects)

def start_game (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code

    Returns a string, representing all usernames separated by ","
    """
    pass