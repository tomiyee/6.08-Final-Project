import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def get_bluffs (request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code
      String user      - (Optional) The user requesting the list of bluffs

    If the user's name is provided, their submission and any matching submissions
    are not included in the return result. This prevents them from receiving
    points for voting for their own bluff.

    Returns a comma-separated string of bluffs in alphabetical order
    """

    if 'room_code' not in request['values']:
        return "Misssing Room Code"
    room_code = request['values']['room_code'].strip()

    # Read the Room Data
    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    conn.commit()
    conn.close()

    if len(room_rows) == 0:
        return "No room with room code: " + room_code

    room_data = json.loads(room_rows[0][0])
    game_data = room_data['game_data']
    player_data = room_data['player_data']

    if game_data['in_lobby']:
        return "No bluffs to list"

    # Builds a list of bluffs, without repetition
    bluffs = set()

    # Fetches the correct answer
    round_number, question_number = game_data['round_number'], game_data['question_number']
    word_number = (round_number - 1) * 3 + question_number - 1
    current_word, current_meaning, current_ans = game_data['all_prompts'][word_number]
    bluffs.add(current_ans)

    # Fetches the Player Submitted Answers
    for player in room_data['player_data']:
        if not room_data['player_data'][player]['submitted']:
            bluffs.add("No Submission")
        else:
            bluffs.add(room_data['player_data'][player]['submission'])

    # If user is provided, remove their submission before returning
    if 'user' in request['values']:
        user = request['values']['user']
        bluffs.remove(room_data['player_data'][user]['submission'])

    # Joins the list of strings with commas in between.
    return ",".join(sorted(list(bluffs)))
