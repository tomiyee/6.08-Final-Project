import json
import sqlite3

bluffalo_db = '__HOME__/bluffalo/game_data.db'
# Note json.load(String) and json.dumps(Objects)

def join_room (request):
    """
    Given the POST request with:
      String room_code - The characters that rep the room code
      String user      - The name of the player entered on ESP

    Returns a string, representing all usernames separated by ","
    """

    conn = sqlite3.connect(bluffalo_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor() 
    
    #data from request: room code, player user name, and their bluff submitted
    room_code = request['form']['roomcode']
    user = request['form']['username'] 
    
    connection.execute('''CREATE TABLE IF NOT EXISTS game_table (roomcode text, Player_and_Room_data text);''')

    room_json = connection.execute('''SELECT * FROM game_table WHERE roomcode = ?;''', (room_code,))
    # Fetch the JSON String from the SQL with the right room code
    
    # json load: turns json file into python dictionary
    room = json.load(room_json)
    room['player_data'][user]["score"] = 0
    room['player_data'][user]["submitted"] = False
    room['player_data'][user]["submission"] = None
    
    # json dump: turns dictionary to json thing
    new_room_json = json.dumps(room)
        
    #update SQL with updated json room data
    connection.execute('''UPDATE game_table SET Player_and_Room_data =? WHERE roomcode =?;''', (new_room_json, room_code))
    
    players = [player for player in room['player_data']]
    
    return str(players) #string representing all usernames separated by ","

  
    

