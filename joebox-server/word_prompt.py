import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.load(String) and json.dumps(Objects)

def current_prompt (request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns a string in the format "WORD=PROMPT"
    """

    try:
        room_code = request['values']['room_code']
    except:
        return "Invalid room code"

    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()

    try:
        room_json_string = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?''', (room_code,)).fetchall()[0]
    except:
        conn.commit()
        conn.close()
        return "Room code does not exist."

    room_json = json.load(room_json_string)
    game_data = room_json['game_data']
    current_word, current_meaning = game_data['Current_word'], game_data['Current_meaning']
    conn.commit()
    conn.close()
    return '{}={}'.format(current_word, current_meaning)
        
        
