# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 23:08:10 2020

@author: kgao1
"""

import json 

def submit_bluff (request):
   request should have:
      user = ... 
      room_code = ...
      bluff = ... 

   room_json = Fetch the JSON String from the SQL with the right room code 
   room = json.load(room_json) #converts players data string into dictionary
   Set room[“player_data”][user].submitted = True
   Set room[“player_data”][user].submission = bluff

   If all players.submitted = True
     Set room[“game_data”].waiting_for_submissions = False

   Update SQL with updated json room data
   new_room_json = 
  # new_room_json = json.dumps(room)

#json load: turns json file into python dictionary
#json dump: turns dictionary to json thing
   return number people not submitted
   



#SQL database: 2 columns: one with roomcode, and one as json dictionary of player data
#column one: roomcode
#all room data column of sql database: 
{
  “player_data”: {
    “Joe 1”: {
       “Score”: 0,
       “Submitted”: False,
       “Submission”: None,   
    }
    “Joe 2”: {
       “Score”: 100,
       “Submitted”: True,
       “Submission”: “Help”
    }
  },

  “game_data”: {
    In_lobby: False,
    Current_word: “babble”,
    Current_meaning: “to ___ on and on”,
    Current_answer: “drone”,
    Round_number: 2,
    Question_number: 3,
    Selecting_options: true
  }
}
