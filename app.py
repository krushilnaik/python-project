"""
Smoothstack Evaluation Week Final Project
"""
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from openpyxl import load_workbook
from pydantic import ValidationError
from werkzeug.utils import secure_filename

import utils.helpers as helpers
from models import db
from models.summary import Summary
from utils.constants import (ARCHIVE, ERROR, SUMMARY_SHEET, UPLOADS,
                             VALID_SHEETS, VOC_SHEET)
from utils.logger import error, info

# load environment variables
load_dotenv()

app = Flask(__name__)

HOST = os.getenv("MYSQL_HOST")
USER = os.getenv("MYSQL_USER")
DATABASE = os.getenv("MYSQL_DATABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USER}@{HOST}/{DATABASE}"
app.secret_key = "55e36cb88d9251f1bd812ec5242e5ead"

db.init_app(app)

with app.app_context():
    db.create_all()

# create the above directories if they don't exist
for _dir in [UPLOADS, ARCHIVE, ERROR]:
    _dir.mkdir(parents=True, exist_ok=True)
info("Created storage directories")


@app.get('/health')
def check():
    """
    Ping this route to make sure the server is up and running

    Returns:
        str: "OK" if the request successfully hit the server
    """

    return "Ok"


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

    file = request.files["file"]

    if not file.filename:
        flash("No file uploaded")
        return redirect(url_for('index'))

    # cleanse file path of crazy characters
    filename = secure_filename(file.filename)

    # check if file has already been parsed
    if helpers.has_been_parsed(filename):
        return redirect(url_for('index'))

    file.save(UPLOADS / filename)

    # try to infer month and year from file. If not possible, move to ERROR
    try:
        (month, year) = helpers.get_month_year(filename)
    except (KeyError, ValueError) as err:
        helpers.file_to_errors(filename, err)
        flash("Error: malformed speadsheet")
        return redirect(url_for("index"))

    # parse file with openpyxl
    workbook = load_workbook(UPLOADS / filename, data_only=True)

    # check if all three tabs are present (if not, move to ERROR)
    if len(workbook.sheetnames) != 3 or set(workbook.sheetnames) != VALID_SHEETS:
        flash("Error: malformed speadsheet")
        helpers.file_to_errors(
            filename, f"{filename} doesn't have the expected sheets"
        )
        return redirect(url_for("index"))

    try:
        active_sheet = workbook[SUMMARY_SHEET]
        data_columns = ["A", "B", "C", "D", "E", "F"]

        # A well formed sheet has relavent data in rows 2 to 14 (for the 12 months)
        for num in range(2, 14):
            values = [active_sheet[f"{c}{num}"].value for c in data_columns]

            helpers.validate_and_write(values)

        info(f"Searching summary table for info on {year}-{month}")

        summary = Summary.get_entry(year, month)

        active_sheet = workbook[VOC_SHEET]

        # finished processing, move file to ARCHIVE
        # and return a view with the data
        helpers.file_to_archives(filename)

        return render_template("results.html", value=summary.as_dict())
    except ValidationError as err:
        flash(f"Some of the data in {filename} is invalid!")
        helpers.file_to_errors(filename, err)
        return redirect(url_for("index"))


@app.errorhandler(404)
def invalid_route(err):
    """
    Catch-all route for any unrecognized URLs

    Returns:
        Template: Custom 404 page
    """

    error(err)
    return render_template('404.html')
