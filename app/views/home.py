from flask import render_template, request
from flask_socketio import emit, disconnect
from app import app, socketio


@app.route('/')
def index():
    print("CONNECTED!!")
    return render_template('home.html')
