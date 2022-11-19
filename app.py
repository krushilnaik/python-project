"""
Smoothstack Evaluation Week Final Project
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.errorhandler(500)
def invalid_route(e):
    return render_template('500.html')


if __name__ == "__main__":
    pass
