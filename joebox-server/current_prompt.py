import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def current_prompt (request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns a string in the format "WORD=PROMPT"
    """

    try:
        room_code = request['values']['room_code'].strip()
    except:
        return "Invalid room code"

    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()
    rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?''', (room_code,)).fetchall()
    conn.commit()
    conn.close()

    if not rows:
        return "Room code does not exist."

    room_json_string = rows[0][0]
    room = json.loads(room_json_string)


    game_data = room['game_data']
    # current_word, current_meaning = game_data['current_word'], game_data['current_meaning']

    round_number, question_number = game_data['round_number'], game_data['question_number']
    word_number = (round_number-1)*3+question_number-1
    current_word, current_meaning, current_ans = game_data['all_prompts'][word_number]

    return '{}={}'.format(current_word, current_meaning)
