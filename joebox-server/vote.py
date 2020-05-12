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

    room_code = request_form['room_code'].strip()
    user = request_form['user'].strip()
    choice_index = int(request_form['choice'])

    # Connect to the SQL Database and try to find the room_code
    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    # Return an error if there is not a room with the room code
    if len(room_rows) == 0:
        conn.commit()
        conn.close()
        return "Room does not exist"

    # Loads the dictionary and the short cut variables
    room_data = json.loads(room_rows[0][0])
    game_data = room_data['game_data']
    player_data = room_data['player_data']

    # Generates the set of alphebetically sorted bluffs
    bluffs = set()
    for player in player_data:
        if not player_data[player]['submitted']:
            bluffs.add("No Submission")
        else:
            bluffs.add(player_data[player]['submission'])
    bluffs.remove(player_data[user]['submission'])
    # Add the Correct Answer
    round_number, question_number = game_data['round_number'], game_data['question_number']
    word_number = (round_number - 1) * 3 + question_number - 1
    current_word, current_meaning, current_ans = game_data['all_prompts'][word_number]
    bluffs.add(current_ans)
    # Sorts all the options in alphabetical order
    bluffs = sorted(list(bluffs))

    if bluffs[choice_index] == current_ans:
        player_data[user]['voted_correctly'] = True

    # Finds all players whose bluff was the choice and appends the name of the user
    for player in player_data:
        if not player_data[player]['submitted']:
            continue
        if room_data['player_data'][player]['submission'] == bluffs[choice_index]:
            room_data['player_data'][player]['votes_received'].append(user)

    # records that the user has votes
    player_data[user]['voted'] = True

    # Count number of people who have not voted
    num_no_vote = len([p for p in player_data if not player_data[p]['voted']])

    # Handle Transition to Submission State
    if num_no_vote == 0:
        # Reset the Submission Status of all the players in the game
        for player in room_data['player_data']:
            player_data[player]['submitted'] = False

        # Toggle the Game State Variables
        room_data["game_data"]['waiting_for_votes'] = False
        room_data["game_data"]['waiting_for_submissions'] = True

        # Tally Scores
        for player in player_data:
            # Points for fooling others
            player_data[player]['score'] += (
                500 * game_data['round_number'] * len(room_data['player_data'][player]['votes_received']))
            # Points for right answer
            player_data[player]['score'] += (
                1000 * player_data[player]['voted_correctly']) * game_data['round_number']

        # Move on to next question
        if game_data['question_number'] == 3:
            game_data['round_number'] += 1
            game_data['question_number'] = 1
        elif game_data['round_number'] == 3:
            # Begin endgame
            room_data["game_data"]['waiting_for_submissions'] = False
            room_data["game_data"]['in_lobby'] = True
            pass
        else:
            game_data['question_number'] += 1

    new_room_json = json.dumps(room_data)

    connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code)).fetchall()
    conn.commit() # commit commands
    conn.close() # close connection to database
    return 'There are ' + str(num_no_vote) +  ' player(s) who have not voted this round'
