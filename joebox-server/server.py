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
        if action == "initialize_game_db":
            return initialize_game_db()
        if action == "join_room":
            return join_room(request)
        if action == "start_game":
            return start_game(request)
        if action == "submit_bluff":
            return submit_bluff(request)

    return "Unhandled action: " + action + ". Double check the action is spelled correctly."

def initialize_game_db ():
    """
    Initialize an SQL DB at the location bluffalo_db with 2 cols
    first col being room_code TEXT, and second being room_data TEXT
    """
    conn = sqlite3.connect('__HOME__/bluffalo/game_data.db')  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)
    connection.execute('''CREATE TABLE IF NOT EXISTS game_table (room_code text, game_data text);''') # run a CREATE TABLE command
    connection.execute('''INSERT into game_table VALUES (?,?);''', (
        "ABCD", '''
        {
          "player_data": {
            "Joe 1": {
               "score": 0,
               "submitted": false,
               "submission": null
            },
            "Joe 2": {
               "score": 100,
               "submitted": true,
               "submission": "Help"
            }
          },

          "game_data": {
            "in_lobby": false,
            "current_word": "acinaceous",
            "current_meaning": "full of _____",
            "current_answer": "kernels",
            "round_number": 2,
            "question_number": 3,
            "waiting_for_submissions": true,
            "selecting_options": false
          }
        }
    '''))
    conn.commit() # commit commands
    conn.close() # close connection to database
    return "Created the db with one sample game"
