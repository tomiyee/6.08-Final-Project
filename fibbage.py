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
        user = request["form"]["user"] #name of newly posted item (the item we're adding to cart from post request)
        room_code = request["form"]["room"] #total price of items added this time to our cart
        score = request["form"]["score"]
        word = request["form"]["word"]
        
        #create online table that stores our items in cart if it doesn't exist
        connection.execute('''CREATE TABLE IF NOT EXISTS new_table (user text, roomcode integer, score integer, word user);''') # run a CREATE TABLE command  
        
        #insert into our table the new item name and it's price in total
        connection.execute('''INSERT into new_table VALUES (?,?,?,?);''', (user, room_code, score, word))
        
        #retrieve all entries from table (all the past item inserts and their prices) for printing out the cart
        entries = connection.execute('''SELECT * FROM new_table;''').fetchall()
        
        #if we want to insert items into cart instead of clearing cart
        if word != "CLEAR":
            to_display = "" #the string with current tally of items in cart we want to return to be printed on our lcd screen 
            total_price = 0 #total price of all items in cart so far
                for item_name, price in entries: #iterate through all items and their prices in our cart
                    to_display += item_name #add name in string form of the item name
                    to_display += " "*(14 - len(item_name)) #space between item name and it's price for display purposes to look uniform
                    to_display += "$"
                    formatted_price = round(price, 2) #round price to two decimal places
                    to_display += str(formatted_price) + "\n" #add new line each time we move on to the next entry in our table
                    total_price += price #add price of the current item to total price
                    
            to_display += "Total price:  $"
            formatted_price = round(total_price, 2)
            to_display += str(formatted_price)
            
            conn.commit() # commit commands
            conn.close() # close connection to database
            return to_display
        else: #clear database if the command was to clear (checkout/reset cart)
            connection.execute("DROP TABLE IF EXISTS new_table") #delete table to reset cart (if the table exists that is)

            conn.commit() #commit commands
            conn.close() #close connection to database
            return 'cleared database!' #for debugging purposes on the arduino Serial Monitor

