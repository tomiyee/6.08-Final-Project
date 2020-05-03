import json
import sqlite3
import os
import random

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

token_length = 8;

def join_room (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code
      String user      - The name of the player entered on ESP
      String token     - (Optional) The token unique to the player (for reconnect)

    tl;dr -> Join 1st time with room_code and user. Save the token you receive
             Join 2nd time with room_code, user, and token

    If no token is provided:
        1. Checks if the username is valid (only capital letters)
        2. Searches for a player that shares the given token
        3. If a player is found, throw an error.
        4. If the game is not currently in the lobby, throw an error
        5. Creates the empty player data
        6. Generates a unique token for the player data
        7. Returns "Token: <8_char_token>"

    If a token is provided:
        1. Checks if the username is valid (only capital letters)
        2. Searches for a player that shares the given token
        3. If a player is found, replace the old username with new username.
           Usually, the username should be the same. If they don't match,
           then we will consider it a request to "change username."
        4. Allow the username to join the game regardless of state
        4. Returns "Token: (8_char_token)" if all is successful

    Returns the user's unique token in the string format "Token: <8_char_token>"
    """

    # data from request: room code, player user name, and their bluff submitted
    # one of the parameters in POST missing
    if 'room_code' not in request['form']:
        return "Missing Room Code"
    if 'user' not in request['form']:
        return "Missing Username"

    room_code = request['form']['room_code']
    user = request['form']['user']

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVQXYZ"
    for c in user:
        if c not in alphabet:
            return "Username can only have capital letters."

    # connect to that database (will create if it doesn't already exist)
    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()
    # Fetch the JSON String from the SQL with the right room code
    rooms_json = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()

    # room does not exist yet
    if len(rooms_json) == 0:
        conn.commit()
        conn.close()
        return 'Room does not exist.'

    # there are more than one room with this room code
    if len(rooms_json) > 1:
        conn.commit()
        conn.close()
        return 'Multiple rooms with this room code exist'

    # json load: turns json file into python dictionary
    room = json.loads(rooms_json[0][0])

    # Prioritize Handling the Token First
    if 'token' in request['form']:
        token = request['form']['token']
        player_with_token = None
        for player in room['player_data']:
            if room['player_data'][player]['token'] == token:
                player_with_token = player
                break
        if player_with_token == None:
            conn.commit()
            conn.close()
            return "No player with the token: " + token

        # If the names don't match, take the new username, remove old player
        if player_with_token != user:
            for player in room['player_data']:
                if player == user:
                    conn.commit()
                    conn.close()
                    return "Username already exists"
            room['player_data'][user] = room['player_data'][player_with_token]
            room['player_data'].pop(player_with_token, None)

            new_room_json = json.dumps(room)
            #update SQL with updated json room data
            connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code))
        conn.commit()
        conn.close()
        return "Token: " + token

    # ------> No Token from here onwards

    # can't join room under the same username, username already exists
    if user in room['player_data']:
        conn.commit()
        conn.close()
        return 'Username already exists'

    # can't join room while game is not in lobby
    if not room['game_data']['in_lobby']:
        conn.commit()
        conn.close()
        return 'Game is not in lobby'

    existing_tokens = set()
    for player in room['player_data']:
        existing_tokens.add(room['player_data'][player]['token'])

    # Generate a random token to uniquely ID this player
    token = "";
    for i in range(token_length):
        token += random.choice (alphabet)
    # If there is a conflict, repeat until not conflicting
    while token in existing_tokens:
        token = ""
        for i in range(token_length):
            token += random.choice (alphabet)

    # Initializes a simple dictionary for the user
    room['player_data'][user] = {
       "score": 0,
       "voted": False,
       "voted_correctly": False,
       "submitted": False,
       "submission": None,
       "votes_received": [],
       "token": token
    }

    # json dump: turns dictionary to json thing
    new_room_json = json.dumps(room)

    #update SQL with updated json room data
    connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code))
    conn.commit()
    conn.close()

    return "Token: " + token
