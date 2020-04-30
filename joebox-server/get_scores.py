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

    # Temporary Return Value
    return "Player1,100,Player2,200,Player3,150"
