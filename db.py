import sqlite3

def get_db():

    db = sqlite3.connect('TodoDB.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )

    db.row_factory = sqlite3.Row
    return db


def close_db(db=None):

    if db is not None:
        db.close()
