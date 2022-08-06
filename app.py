from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/Login/", methods = ['GET', 'POST'])
def login():
    if request.methods == 'POST':

        return
    
    return render_template()

