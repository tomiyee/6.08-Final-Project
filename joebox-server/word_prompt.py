import json
import sqlite3

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.load(String) and json.dumps(Objects)

def current_prompt (request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns a string in the format "WORD=PROMPT"
    """

    pass
