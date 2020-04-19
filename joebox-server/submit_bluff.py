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

    Returns String "None" if failed to add
    Returns number of people who haven't submitted bluff yet if successfully added
    see number of people who haven't submitted a bluff yet in Postman
    """
    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor() 
    
    #data from request: room code, player user name, and their bluff submitted
    room_code = request['form']['roomcode']
    user = request['form']['user_name'] 
    bluff_submitted = request['form']['bluff'] # text submission user entered on ESP
    
    connection.execute('''CREATE TABLE IF NOT EXISTS game_table (roomcode text, Player_and_Room_data text);''')
    try: 
        room_json = connection.execute('''SELECT * FROM game_table WHERE roomcode = ?;''', (room_code,))
        # Fetch the JSON String from the SQL with the right room code
        
        # json load: turns json file into python dictionary
        room = json.load(room_json)
        room['player_data'][user]["submitted"] = True
        room['player_data'][user]["submission"] = bluff_submitted
        
        all_players_submitted = True
        num_no_submission = 0 #players who haven't submitted yet
        for player in room['player_data']: 
            if player['submitted'] == False: 
                all_players_submitted = False
                num_no_submission += 1
            
        if all_players_submitted: #if all players submitted
            room['game_data']['waiting_for_submissions'] = False
            room['game_data']['selecting_options'] = True   
    
        # json dump: turns dictionary to json thing
        new_room_json = json.dumps(room)
        
        #update SQL with updated json room data
        connection.execute('''UPDATE game_table SET Player_and_Room_data =? WHERE roomcode =?;''', (new_room_json, room_code))
        return num_no_submission #if successfully added
    except: #if not successfully added
        return 'None'

    #test using post request in postman: put all content under post body
    