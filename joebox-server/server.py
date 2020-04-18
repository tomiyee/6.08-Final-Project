import numpy as np
import time
import datetime
import sqlite3
import json
import sys
sys.path.append('__HOME__/bluffalo')
# import individual action handlers
from game_check import in_lobby, room_code_check
from word_prompt import current_prompt
from join_room import join_room
from start_game import start_game
from submit_bluff import submit_bluff

# The database with game data for everyone
bluffalo_db = '__HOME__/bluffalo/game_data.db'

def request_handler (request) :
    if request['method'] == 'GET':
        if 'action' not in request['args']:
            return "Error: All requests need an 'action.'"
        # Determines which action the http request wants done
        action = request['values']['action']
        # Selects the correct handler for the action
        if action == "in_lobby":
            return in_lobby(request)
        if action == "room_code_check":
            return room_code_check(request)
        if action == "current_prompt":
            return current_prompt(request)

    if request['method'] == 'POST':
        if 'action' not in request['form']:
            return "Error: All requests need an 'action.'"
        # Determines which action the http request wants done
        action = request['form']['action']
        # Selects the correct handler for the action
        if action == "join_room":
            return join_room(request)
        if action == "start_game":
            return start_game(request)
        if action == "submit_bluff":
            return submit_bluff(request)

    return "Unhandled action: " + action + ". Double check the action is spelled correctly."

def initialize_game_db ():
    """
    TO-DO - Initialize an SQL DB at the location bluffalo_db with 2 cols
    first col being room_code TEXT, and second being room_data TEXT
    """

    pass
