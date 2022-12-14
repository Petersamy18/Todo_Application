from multiprocessing import connection
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
    connection = get_db()
    connection.execute(
        f"Insert into User (Email, Username, Hashed_Password) values('{email}', '{name}', '{h_pass}')")
    connection.commit()
    close_db(connection)


def retreive_tasks(id):
    connection = get_db().cursor()
    connection.execute(
        f"select * from Task WHERE  User_id={id} ")
    data = connection.fetchall()
    close_db(connection)
    return data


def insert_Task(title, descr, id):
    connection = get_db()
    connection.execute(
        f"Insert into Task (Title, Describtion, status, User_id) values('{title}', '{descr}', 'Not Done', {id})")
    connection.commit()
    close_db(connection)

def update_task(title,descr,status,id):
    connection = get_db()
    connection.execute(f"""UPDATE Task SET Title="{title}", Describtion="{descr}", status="{status}" WHERE Task_id={id};""")
    connection.commit()
    close_db(connection)

def retreive_task(id):
    connection = get_db().cursor()
    connection.execute(
        f"select * from Task WHERE task_id={id}")
    data = connection.fetchone()
    close_db(connection)
    return data

def delete_task(id):
    connection = get_db()
    connection.execute(f"Delete from Task WHERE task_id={id}")
    connection.commit()
    close_db(connection)

