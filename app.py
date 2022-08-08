from asyncio import Task
from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from flask import request
from flask import session, g
from db import get_db, close_db, retreive_tasks, retreive_users, insert_user, insert_Task, update_task, retreive_task, delete_task
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = 'MazenAndPeterExampleforsecretkey'

# a function runs before dealing with any request


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        all_users = retreive_users()
        user = [x for x in all_users if x['User_id'] == session['user_id']][0]
        g.user = user


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/Home/", methods=['GET', 'POST'])
def home():
    # if there is no sessions
    if not g.user:
        return redirect(url_for('login'))

    return render_template('home.html')


@app.route("/Login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            session.pop('user_id', None)
            username = request.form['username']
            password = request.form['password']

            all_users = retreive_users()
            # here we have a row in database which matches the entered username
            user = [x for x in all_users if x['Username'] == username][0]
            if user and check_password_hash(user['Hashed_Password'], password):
                session['user_id'] = user['User_id']
                return redirect(url_for('home'))  # Happy scenario

            # here for example, We should output some messages indicating error while signing in (Try: Message flashing)
            return redirect(url_for('login'))

        except Exception as err:
            print(err)
            return render_template('login.html')

    # if the method == 'GET'
    return render_template('login.html')


@app.route("/signUp/", methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            hash_password = generate_password_hash(password)
            insert_user(email, username, hash_password)
            return redirect(url_for('login'))

        except Exception as err:
            print(err)
            return render_template('sign-up.html')

    return render_template('sign-Up.html')


@app.route("/addTask/", methods=['GET', 'POST'])
def addTask():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            insert_Task(title, description, g.user['User_id'])
            return redirect(url_for('viewTasks'))
        except Exception as err:
            print(err)
            return render_template('addTask.html')
    return render_template('addTask.html')


@app.route("/viewTasks/", methods=['GET', 'POST'])
def viewTasks():
    tasks = retreive_tasks(g.user['User_id'])
    return render_template('viewTasks.html', tasks=tasks)

@app.route("/updateTask/<int:id>", methods=['GET', 'POST'])
def updateTask(id=None):
    if request.method == "POST":
        taskTitle = request.form['title']
        description = request.form['description']
        status = request.form['status']
        update_task(taskTitle,description,status,id)
        return redirect(url_for('viewTasks'))
    task = retreive_task(id)
    return render_template('updateTask.html',task=task)

@app.route("/deleteTask/<int:id>", methods=['GET', 'POST'])
def deleteTask(id=None):
    delete_task(id)
    return redirect(url_for('viewTasks'))