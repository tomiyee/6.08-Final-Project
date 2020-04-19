import json
import sqlite3

bluffalo_db = '__HOME__/bluffalo/game_data.db'
# Note json.load(String) and json.dumps(Objects)

def submit_bluff (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code
      String user      - The name of the player entered on ESP
      String bluff     - The text submission that the user entered on the ESP

    Returns an error code if failed to add:
    -1: unknown error, don't know what happened
    1: if they already submitted a bluff this round
    2: game in lobby, can't submit bluffs right now
    3: game not waiting for submissions, can't submit bluff right now
    8: player doesn't exist in game
    9: one of the required parameters for post request is missing
    Returns number of people who haven't submitted bluff yet if successfully added
    see number of people who haven't submitted a bluff yet in Postman
    """
    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()

    #data from request: room code, player user name, and their bluff submitted

    try:
        room_code = request['form']['roomcode']
        user = request['form']['user_name']
        bluff_submitted = request['form']['bluff'] # text submission user entered on ESP
    except:
        conn.commit() # commit commands
        conn.close() # close connection to database
        return '9' #one of the required parameters are missing

    try: 
        room_json = connection.execute('''SELECT game_data FROM game_table WHERE room_code = ?;''', (room_code,))[0][0]
        # Fetch the JSON String from the SQL with the right room code

        # json load: turns json file into python dictionary
        room = json.load(room_json)

        if user not in room['player_data']:
            return '8' #player doesn't exist in game
        if room['player_data'][user]["submitted"]:
            conn.commit() # commit commands
            conn.close() # close connection to database
            return '1'  #Player already submitted a bluff this round

        if room['game_data']['in_lobby']:
            conn.commit() # commit commands
            conn.close() # close connection to database
            return '2' #in lobby right now, can't submit bluffs

        if not room['game_data']['waiting_for_submissions']:
            conn.commit() # commit commands
            conn.close() # close connection to database
            return '3' #not waiting for submissions, can't submit bluffs right now


        room['player_data'][user]["submitted"] = True
        room['player_data'][user]["submission"] = bluff_submitted

        all_players_submitted = True
        num_no_submission = 0 #players who haven't submitted yet
        for player in room['player_data']:
            if not player['submitted']:
                all_players_submitted = False
                num_no_submission += 1

        if all_players_submitted: #if all players submitted
            room['game_data']['waiting_for_submissions'] = False
            room['game_data']['selecting_options'] = True

        # json dump: turns dictionary to json thing
        new_room_json = json.dumps(room)

        #update SQL with updated json room data
        connection.execute('''UPDATE game_table SET game_data =? WHERE room_code =?;''', (new_room_json, room_code))
        conn.commit() # commit commands
        conn.close() # close connection to database
        return num_no_submission #if successfully added

    except: #if not successfully added
        conn.commit() # commit commands
        conn.close() # close connection to database
        return '-1' #don't know what happened

    #test using post request in postman: put all content under post body
