import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def create_room (request):
    """
    Given the POST request with no required parameters:

    Generates a json with no players yet. It is initialized to have no players.

    Returns the room code, made of 4 capital letters (e.g. ABCD)
    """

    new_room = {
      "player_data": {},
      "game_data": {
        "in_lobby": True,
        "current_word": None,
        "current_meaning": None,
        "current_answer": None,
        "round_number": 1,
        "question_number": 1,
        "waiting_for_submissions": False,
        "selecting_options": False
      }
    }

    # Generate a random room code
    room_code = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(4)])

    # insert the new_room to the room_code

    return room_code
