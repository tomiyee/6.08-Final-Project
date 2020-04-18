import json
import sqlite3

bluffalo_db = '__HOME__/bluffalo/game_data.db'
# Note json.load(String) and json.dumps(Objects)

def room_code_check(request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns the string "None" if no room, and the room code if the room exists
    """

    pass

def in_lobby(request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns the string "None" if not in lobby, and the room code if in lobby
    """

    pass
