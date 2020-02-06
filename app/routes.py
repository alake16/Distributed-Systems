from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


# General Landing Page
@app.route('/')
def index():
    return render_template("index.html", title="Home")


# Admin Landing Page
@app.route('/admin')
def admin():
    return render_template("admin.html", title="Admin")


# Quiz Taker Landing Page
@app.route('/taker')
def taker():
    return render_template("taker.html", title="Taker")


# Quiz Taker Landing Page
@app.route('/player/<sessionID>')
def takerSession(sessionID):
    # do something with a session ID
    return render_template("taker.html", title="Taker")


@app.errorhandler(404)
def notfound():
    """Serve 404 template."""
    return make_response(render_template("404.html"), 404)
