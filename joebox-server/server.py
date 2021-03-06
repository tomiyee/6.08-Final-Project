import numpy as np
import time
import datetime
import sqlite3
import json
import sys
sys.path.append('__HOME__/bluffalo')
# import individual action handlers
from game_check import in_lobby, room_code_check
from current_prompt import current_prompt
from create_room import create_room
from delete_room import delete_room
from join_room import join_room
from start_game import start_game
from submit_bluff import submit_bluff
from dump_data import dump_data
from list_players import list_players
from get_bluffs import get_bluffs
from vote import vote
from get_scores import get_scores
from waiting_for_votes import waiting_for_votes
from waiting_for_submissions import waiting_for_submissions
from score_rank import score_rank

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
        if action == "waiting_for_submissions":
            return waiting_for_submissions(request)
        if action == "waiting_for_votes":
            return waiting_for_votes(request)
        if action == "room_code_check":
            return room_code_check(request)
        if action == "current_prompt":
            return current_prompt(request)
        if action == "list_players":
            return list_players(request)
        if action == "get_bluffs":
            return get_bluffs(request)
        if action == "get_scores":
            return get_scores(request)
        if action == "dump_data":
            return dump_data(request)
        if action == "score_rank":
            return score_rank(request)
        return "Unhandled GET action: " + action + ". Double check the action is spelled correctly."

    if request['method'] == 'POST':
        if 'action' not in request['form']:
            return "Error: All requests need an 'action.'"
        # Determines which action the http request wants done
        action = request['form']['action']
        # Selects the correct handler for the action
        if action == "initialize_game_db":
            return initialize_game_db()
        if action == "create_room":
            return create_room(request)
        if action == "delete_room":
            return delete_room(request)
        if action == "join_room":
            return join_room(request)
        if action == "start_game":
            return start_game(request)
        if action == "submit_bluff":
            return submit_bluff(request)
        if action == "vote":
            return vote(request)
        return "Unhandled POST action: " + action + ". Double check the action is spelled correctly."

    return "Unhandled action: " + action + ". Double check the action is spelled correctly."

def initialize_game_db ():
    """
    Initialize an SQL DB at the location bluffalo_db with 2 cols
    first col being room_code TEXT, and second being room_data TEXT
    """
    conn = sqlite3.connect('__HOME__/bluffalo/game_data.db')  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)
    connection.execute('''CREATE TABLE IF NOT EXISTS game_table (room_code text, game_data text);''') # run a CREATE TABLE command
    with open('ex_room_data.json', 'r') as file:
        data = file.read().replace('\n', '')
    connection.execute('''INSERT into game_table VALUES (?,?);''', ("ABCD", data))
    conn.commit() # commit commands
    conn.close() # close connection to database
    return "Created the db with one sample game"
