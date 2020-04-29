import json
import sqlite3
import os
import random


bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
word_db = os.path.dirname(__file__) + '/../word-database/word_bank.db'
# Note json.loads(String) and json.dumps(Objects)

def vote (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code
      String user      - The user name of the person who is voting
      Int    choice    - The index of the bluff (0-indexed) in

    Returns number of people who haven't voted yet?
    """

    request_form = request['form']
    if 'room_code' not in request_form:
        return "Misssing Room Code"
    if 'user' not in request_form:
        return "Misssing User Name"
    if 'choice' not in request_form:
        return "Misssing Choice Number"

    room_code = request_form['room_code']
    user = request_form['user']
    choice_index = int(request_form['choice'])

    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()

    if len(room_rows) == 0:
        conn.commit() # commit commands
        conn.close() # close connection to database
        return "Room does not exist"

    # Generates the set of alphebetically sorted bluffs
    bluffs = set()

    room_data = json.loads(room_rows[0][0])

    game_data = room_data['game_data']
    round_number, question_number = game_data['round_number'], game_data['question_number']
    word_number = (round_number-1)*3+question_number-1
    current_word, current_meaning, current_ans = game_data['all_prompts'][word_number]
    bluffs.add(current_ans)

    for player in room_data['player_data']:
        if not room_data['player_data'][player]['submitted']:
            bluffs.add("No Submission")
        else:
            bluffs.add(room_data['player_data'][player]['submission'])
    bluffs.remove(room_data['player_data'][user]['submission'])
    bluffs = sorted(list(bluffs))

    if bluffs[choice_index] == current_ans:
        room_data['player_data'][user]['voted_correctly'] = True

    # Finds all players whose bluff was the choice and appends the name of the user
    for player in room_data['player_data']:
        if not room_data['player_data'][player]['submitted']:
            continue
        if room_data['player_data'][player]['submission'] == bluffs[choice_index]:
            room_data['player_data'][player]['votes_received'].append(user)

    # records that the user has votes
    room_data['player_data'][user]['voted'] = True

    # Check if everyone has finished voting, and if so, increment game number
    # calculate new scores, and clear votes
    num_no_vote = 0
    for player in room_data['player_data']:
        if not room_data['player_data'][player]['voted']:
            num_no_vote += 1
    if num_no_vote == 0:
        # Do something to move on to the next stage. Idk man
        room_data["game_data"]['waiting_for_votes'] = False
        # Tally Scores
        for player in room_data['player_data']:
            # Points for fooling others
            room_data['player_data'][player]['score'] += (
                500 * room_data['game_data']['round_number'] * len(room_data['player_data'][player]['votes_received']))
            # Points for right answer
            room_data['player_data'][player]['score'] += (
                1000 * room_data['player_data'][player]['voted_correctly'])
            # Reset
            room_data['player_data'][player]['votes_received'] = []
            room_data['player_data'][player]['voted'] = False

        # Move on to next question
        if room_data['game_data']['question_number'] == 3:
            room_data['game_data']['round_number'] += 1
            room_data['game_data']['question_number'] = 1
        elif room_data['game_data']['round_number'] == 3:
            # Begin endgame
            pass
        else:
            room_data['game_data']['question_number'] += 1

    new_room_json = json.dumps(room_data)

    connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code)).fetchall()
    conn.commit() # commit commands
    conn.close() # close connection to database
    return 'There are ' + str(num_no_vote) +  ' player(s) who have not voted this round'
