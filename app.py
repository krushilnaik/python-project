"""
Smoothstack Evaluation Week Final Project
"""

from flask import Flask, render_template, jsonify, request, flash, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.get('/health')
def check():
    """
    Ping this route to make sure the server is up and running

    Returns:
        str: "OK" if the request successfully hit the server
    """

    return jsonify({"message": "OK"})


@app.route('/')
def index():
    """
    Home page

    Returns:
        Template: HTML page
    """
    return render_template('home.html')


@app.post("/upload")
def upload():
    """
    POST route to insert Excel data to MySQL

    Returns:
        _type_: _description_
    """

    if "file" not in request.files:
        flash("No file part")

    file = request.files["file"]

    if not file.filename:
        flash("No file uploaded")
        return redirect(request.url)

    filename = secure_filename(file.filename)

    file.save(os.path.join('uploads', filename))

    return "Upload request received"


@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')
