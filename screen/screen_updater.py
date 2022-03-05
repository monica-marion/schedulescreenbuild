import sqlite3

DATABASE = '../database.db'

########### Screen Update Methods ###########






############# Database handling #############
# https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

if __name__ == "__main__":
    pass
