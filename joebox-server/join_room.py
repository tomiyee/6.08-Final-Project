import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def join_room (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code
      String user      - The name of the player entered on ESP

    Returns a string, representing all usernames separated by ","
    Error codes:
    -1: unknown error
    2: room does not exist
    4: username already exists
    5: game not in lobby: can't join right now
    7: there is more than one room with this room code
    9: one of the required parameters for post request is missing
    """


    # data from request: room code, player user name, and their bluff submitted
    # one of the parameters in POST missing
    if 'room_code' not in request['form']:
        return "Missing Room Code"
    if 'user' not in request['form']:
        return "Missing Username"

    room_code = request['form']['room_code']
    user = request['form']['user']

    # connect to that database (will create if it doesn't already exist)
    conn = sqlite3.connect(bluffalo_db)
    connection = conn.cursor()

    # Fetch the JSON String from the SQL with the right room code
    rooms_json = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()

    # room does not exist yet
    if len(rooms_json) == 0:
        conn.commit() # commit commands
        conn.close() # close connection to database
        return 'Room does not exist.'

    # there are more than one room with this room code
    if len(rooms_json) > 1:
        conn.commit() # commit commands
        conn.close() # close connection to database
        return 'Multiple rooms with this room code exist'

    # json load: turns json file into python dictionary
    room = json.loads(rooms_json[0][0])

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

    # Initializes a simple dictionary for the user
    room['player_data'][user] = {}
    room['player_data'][user]["score"] = 0
    room['player_data'][user]["submitted"] = False
    room['player_data'][user]["submission"] = None

    # json dump: turns dictionary to json thing
    new_room_json = json.dumps(room)

    #update SQL with updated json room data
    connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code))
    conn.commit()
    conn.close()

    players = [player for player in room['player_data']]
    out = ''
    for player in players:
        out += player
        out += ','

    return out #string representing all usernames separated by ","
