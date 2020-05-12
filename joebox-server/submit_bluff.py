import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def submit_bluff (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code
      String user      - The name of the player entered on ESP
      String bluff     - The text submission that the user entered on the ESP

    Returns number of people who haven't submitted bluff yet if successfully added
    see number of people who haven't submitted a bluff yet in Postman
    """

    #data from request: room code, player user name, and their bluff submitted
    request_form = request['form']
    if 'room_code' not in request_form:
        return "Misssing Room Code"
    if 'user' not in request_form:
        return "Misssing User Name"
    if 'bluff' not in request_form:
        return "Misssing Bluff to Submit"

    room_code = request_form['room_code'].strip()
    user = request_form['user'].strip()
    bluff_submitted = request_form['bluff'].strip()

    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    # Fetch the JSON String from the SQL with the right room code
    if len(room_rows) == 0:
        conn.commit()
        conn.close()
        return "Room does not exist"

    if len(room_rows) > 1:
        conn.commit()
        conn.close()
        return "There are more than one room with this code"

    # json load: turns json file into python dictionary
    room = json.loads(room_rows[0][0])
    game_data = room['game_data']
    player_data = room['player_data']

    if user not in player_data:
        return "Player doesn't exist in game"

    if player_data[user]["submitted"]:
        conn.commit()
        conn.close()
        return 'Player already submitted a bluff this round'

    if not game_data['waiting_for_submissions']:
        conn.commit()
        conn.close()
        return "Not waiting for submissions, can't submit bluffs right now"

    # Forces the bluff_submitted to be strictly capital letters
    bluff_submitted = bluff_submitted.upper()
    for c in bluff_submitted:
        if c not in "ABCDEFGHIJKLMNOPQRSTUVQXYZ":
            return "Bluff can only have capital letters."

    # Fetches the current prompt
    round_number, question_number = game_data['round_number'], game_data['question_number']
    word_number = (round_number-1)*3+question_number-1
    current_word, current_meaning, current_ans = game_data['all_prompts'][word_number]

    #if player submitted the correct answer
    if bluff_submitted.upper() == current_ans.upper():
        return "You submitted the correct answer! Please change it :)"

    player_data[user]["submitted"] = True
    player_data[user]["submission"] = bluff_submitted.upper()

    # Counts the number of people who have submitted bluffs
    num_no_bluff = len([p for p in player_data if not player_data[p]['submitted']])

    # Handle Transition to Vote State
    if num_no_bluff == 0:
        # Toggle the Game State Variables
        game_data['waiting_for_submissions'] = False
        game_data['waiting_for_votes'] = True
        # Reset the player's voting stats
        for player in room['player_data']:
            player_data[player]['votes_received'] = []
            player_data[player]['voted'] = False

    # json dump: turns dictionary to json thing
    new_room_json = json.dumps(room)

    #update SQL with updated json room data
    connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code)).fetchall()
    conn.commit()
    conn.close()
    return 'There are ' + str(num_no_bluff) +  ' player(s) who have not submitted a bluff this round' #if successfully added
