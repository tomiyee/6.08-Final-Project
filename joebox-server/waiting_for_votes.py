import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def waiting_for_votes (request):
    """
    Given the GET request with:
      String room_code - The characters that represent the room code

    This API call should loop through the player_data object that corresponds
    to the room_code, and if player_data[player]['voted'] is False for any
    player, we should return the string "true".

    Make sure to check for all the false cases, like if we are in the lobby or
    if we are waiting for submissions.

    Returns a comma-separated string of players and their scores
    """

    # Temporary Return Value
    return "false"
