import sqlite3
db = "word_bank.db"

def database_handle_request(word_meaning_answer_tuple_list):
    conn = sqlite3.connect(db)  # connect to that database (will create if it doesn't already exist)
    c = conn.cursor()  # move cursor into database (allows us to execute commands)

    c.execute('''CREATE TABLE IF NOT EXISTS word_table (word text, meaning text, answer text);''') # run a CREATE TABLE command

    for word, meaning, answer in word_meaning_answer_tuple_list:
        c.execute('''INSERT into word_table VALUES (?, ?, ?);''', (word, meaning, answer))

    conn.commit() # commit commands
    conn.close() # close connection to database

    return "done inserting words"

word_list = []
with open('bluffalo_words_with_blank.txt', 'r') as f:

    for line in f:
        word, meaning, answer = line[:-1].split('=')
        word_list.append((word, meaning, answer))


d= database_handle_request(word_list)
print(d)
