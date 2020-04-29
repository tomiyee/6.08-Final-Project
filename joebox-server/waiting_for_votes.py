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

    This API call should access the room data for the room_code, and check if
    the value for "game_data", under "waiting_for_votes" is True. If
    waiting_for_votes is True, then this API call should return "true", and
    "false" otherwise.

    Returns "true" if the game is waiting for votes, and "false" otherwise
    """

    # Temporary Return Value
    return "false"
