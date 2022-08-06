from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/Login/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route("/signUp/", methods=['GET', 'POST'])
def signUp():
    return render_template('sign-Up.html')
