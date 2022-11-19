"""
Smoothstack Evaluation Week Final Project
"""

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "55e36cb88d9251f1bd812ec5242e5ead"

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
        return redirect(url_for('index'))

    file = request.files["file"]

    if not file.filename:
        flash("No file uploaded")
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)

    file.save(os.path.join('uploads', filename))

    # check if file has already been parsed

    # try to infer month and year from file. If not possible, move to ERROR

    # parse file with openpyxl

    # check if all three tabs are present (if not, move to ERROR)

    # write data for that month and year to mysql

    # move file to ARCHIVED and update processed.lst

    return "Upload request received"


@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')
