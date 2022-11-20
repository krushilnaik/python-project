"""
Smoothstack Evaluation Week Final Project
"""

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from openpyxl import load_workbook
from models import db
from models.Summary import Summary
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root@database/smoothstack"
app.secret_key = "55e36cb88d9251f1bd812ec5242e5ead"

db.init_app(app)

with app.app_context():
    db.create_all()

VALID_SHEETS = ["Summary Rolling MoM",
                "VOC Rolling MoM", "Monthly Verbatim Statements"]

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


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

    # parse file with openpyxl

    wb = load_workbook(os.path.join('uploads', filename), data_only=True)

    # check if all three tabs are present (if not, move to ERROR)

    if wb.sheetnames != VALID_SHEETS:
        pass

    SHEET = wb["Summary Rolling MoM"]

    COLUMNS = ["A", "B", "C", "D", "E", "F"]

    for r in range(2, 14):
        values = [SHEET[f"{c}{r}"].value for c in COLUMNS]

        # write data for that month and year to mysql
        row = Summary(
            time_period=values[0],
            calls_offered=values[1],
            abandoned_after_30=values[2],
            fcr=values[3],
            dsat=values[4],
            csat=values[5],
        )

        db.session.add(row)
        db.session.commit()

    # try to infer month and year from file. If not possible, move to ERROR
    try:
        parts = filename.split("_")

        month = MONTHS[parts[-2].lower()[:3]]
        year = parts[-1][:4]

        # move file to ARCHIVED and update processed.lst
        with open("./processed.lst", mode="a") as processed:
            processed.write(filename + "\n")

        return render_template("results.html", value=f'{year}-{month:02}-##')
    except KeyError:
        print("Failed")


@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')
