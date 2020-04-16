# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 23:14:23 2020

@author: kgao1
"""

# -*- coding: utf-8 -*-
"""
Created on Mar Mar 27 12:12:09 2020

@author: kgao1
"""

import sqlite3

fibbage = "fibbage.db" # name of database
visits_db = '__HOME__/design_4/fibbage.db'

def request_handler(request):
    conn = sqlite3.connect(visits_db)  # connect to that database (will create if it doesn't already exist)
    connection = conn.cursor()  # move cursor into database (allows us to execute commands)

    if request["method"] == "POST": #if it's a post request
        user = request["form"]["user"] #user name of player
        room_code = request["form"]["room"] #room code of player
        score = request["form"]["score"] #current score of user
        word = request["form"]["word"] #latest submitted word from the user
        
        #create online table that stores user names, their current score, and latest word if it doesn't exist
        connection.execute('''CREATE TABLE IF NOT EXISTS new_table (user text, roomcode integer, score integer, word text);''') # run a CREATE TABLE command  
        
        #insert into our table updated user stats
        connection.execute('''INSERT into new_table VALUES (?,?,?,?);''', (user, room_code, score, word))
        
        #retrieve all entries from table 
        entries = connection.execute('''SELECT * FROM new_table;''').fetchall()
        
        user_data = {}
        for entry in entries: 
            user_name = entry[0]
            room_code = entry[1]
            score = entry[2]
            word = entry[3]
            user_data[user_name] = (room_code, score, word)
        
        conn.commit() # commit commands
        conn.close() # close connection to database
        return user_data #returns a dictionary of user name and their room code, current score, and latest submitted word


