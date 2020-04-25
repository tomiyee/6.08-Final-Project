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

    # Joins the list of strings with commas in between.
    return ",".join(players)
