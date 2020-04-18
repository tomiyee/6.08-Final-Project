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

    Returns String "Success" if successfully added, String "None" if failed to add
    """

    # room_json = Fetch the JSON String from the SQL with the right room code
    # room = json.load(room_json)
    # Set room[“player_data”][user].submitted = True
    # Set room[“player_data”][user].submission = bluff

    # If all players.submitted = True
    #   Set room[“game_data”].waiting_for_submissions = False
    #   Set room[“game_data”].selecting_options to True

    # Update SQL with updated json room data
    # new_room_json = json.dumps(room)

    # json load: turns json file into python dictionary
    # json dump: turns dictionary to json thing


    pass
