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


def retreive_users():
    connection = get_db().cursor()
    connection.execute("select * from User;")
    data = connection.fetchall()
    close_db(connection)
    return data

def insert_user(email, name, h_pass):
    connection = get_db().cursor()
    connection.execute(f"Insert into User (Email, Username, Hashed_Password) values('{email}', '{name}', '{h_pass}')")
    connection.commit()
    close_db(connection)

