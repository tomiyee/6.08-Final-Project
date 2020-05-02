import json
import sqlite3
import os

bluffalo_db = os.path.dirname(__file__) + '/game_data.db'
# Note json.loads(String) and json.dumps(Objects)

def score_rank (request):
    """
    Given the GET request with:
      String room_code - The characters that rep the room code

    Returns a comma-separated string of players along with their current get_scores
    sorted from highest to lowerst score in the specified room
    """

    #list of tuples of player name and their current score
    scores = []

    if 'room_code' not in request['values']:
        return "Missing Room Code"
    room_code = request['values']['room_code']


    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)
    room_rows = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,)).fetchall()
    conn.commit()
    conn.close()

    if len(room_rows) == 0:
        return "No room with room code: " + room_code

    if len(room_rows) > 1:
        return "More than one room with this room code"

    #dictionary of game and player data for room with given room code
    room_data = json.loads(room_rows[0][0])
    #list of players currently in game
    players = [player for player in room_data['player_data']]
    for player in room_data['player_data']:
        scores.append((player, room_data['player_data'][player]['score']))

    if len(players) == 0:
        return "No players in game currently"

    #list of tuples with the player name and their current score
    sorted_scores = sorted(scores, key = lambda x: x[1])

    outstr = [] #list for printing purposes
    for tup in sorted_score:
        outstr.extend(tup[0])
        outstr.extend(tup[1])

    # Joins the list of strings with commas in between.
    return ",".join(putstr)
