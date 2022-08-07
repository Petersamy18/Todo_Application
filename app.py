from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from flask import request
from flask import session, g
from db import get_db, close_db, retreive_users, insert_user
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
app.secret_key = 'MazenAndPeterExampleforsecretkey'

#a function runs before dealing with any request 
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        all_users = retreive_users()
        user = [x for x in all_users if x['User_id']== session['user_id']][0]
        g.user = user


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/Home/", methods=['GET', 'POST'])
def home():
    #if there is no sessions
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
            user = [x for x in all_users if x['Username']== username][0]  #here we have a row in database which matches the entered username
            if user and check_password_hash(user['Hashed_Password'], password):
                session['user_id'] = user['User_id']
                return redirect(url_for('home')) #Happy scenario

            # here for example, We should output some messages indicating error while signing in (Try: Message flashing)
            return redirect(url_for('login')) 

        except Exception as err:
            print(err)
            return render_template('login.html')

    #if the method == 'GET'        
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
