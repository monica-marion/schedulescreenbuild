import sqlite3
import flask

DATABASE = '../database.db'

################### Flask ###################






############# Database handling #############
# https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
