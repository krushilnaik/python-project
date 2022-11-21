"""
Smoothstack Evaluation Week Final Project
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from openpyxl import load_workbook
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from models import db
from models.summary import Summary
from utils.constants import (ARCHIVE, ERROR, MONTHS, SUMMARY_SHEET, UPLOADS,
                             VALID_SHEETS)
from utils.helpers import file_to_archives, file_to_errors, validate_and_write

# load environment variables
load_dotenv()

app = Flask(__name__)

HOST = os.getenv("MYSQL_HOST")
USER = os.getenv("MYSQL_USER")
DATABASE = os.getenv("MYSQL_DATABASE")

# set up logging

file_handler = RotatingFileHandler('flask-student-info.log',
                                   maxBytes=16384,
                                   backupCount=20)
file_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [@%(filename)s:%(lineno)d]'
)

file_handler.setFormatter(file_formatter)

app.logger.addHandler(file_handler)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USER}@{HOST}/{DATABASE}"
app.secret_key = "55e36cb88d9251f1bd812ec5242e5ead"

db.init_app(app)

with app.app_context():
    db.create_all()

# create the above directories if they don't exist
for _dir in [UPLOADS, ARCHIVE, ERROR]:
    _dir.mkdir(parents=True, exist_ok=True)
app.logger.info("Created storage directories")


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
    with open('processed.lst', 'a+', encoding="utf-8") as processed:
        # jump to the start of the file to begin reading
        processed.seek(0)

        if filename in processed.read():
            flash(f"{filename} has already been processed")
            app.logger.info(f"{filename} has already been processed")
            return redirect(url_for('index'))
        else:
            app.logger.info(f"Starting to process {filename}")
            processed.write(filename + "\n")

    file.save(UPLOADS / filename)

    # try to infer month and year from file. If not possible, move to ERROR
    try:
        parts = filename.split("_")[-2:]
        month = MONTHS[parts[0].lower()[:3]]
        year = parts[1][:4]

        if not year.isnumeric():
            raise ValueError("Year could not be inferred from file name")
    except (KeyError, ValueError) as error:
        file_to_errors(filename, error)
        app.logger.error(error)

        flash("Error: malformed speadsheet")
        return redirect(url_for("index"))

    # parse file with openpyxl
    workbook = load_workbook(UPLOADS / filename, data_only=True)

    # check if all three tabs are present (if not, move to ERROR)
    if len(workbook.sheetnames) != 3 or set(workbook.sheetnames) != VALID_SHEETS:
        flash("Error: malformed speadsheet")
        file_to_errors(filename)
        app.logger.error(f"Some required sheets are missing!")
        return redirect(url_for("index"))

    active_sheet = workbook[SUMMARY_SHEET]
    data_columns = ["A", "B", "C", "D", "E", "F"]

    try:
        # A well formed sheet has relavent data in rows 2 to 14 (for the 12 months)
        for num in range(2, 14):
            values = [active_sheet[f"{c}{num}"].value for c in data_columns]

            validate_and_write(values)

        app.logger.info(f"Searching database for info on {year}-{month}")

        # fetch the first entry found that was recorded on the month in question
        # (between the 1st and 31st of that month)
        test = Summary.query.filter(Summary.time_period.between(
            f'{year}-{month}-01', f'{year}-{month}-31')
        ).first()

        # finished processing, move file to ARCHIVE
        # and return a view with the data
        file_to_archives(filename)
        app.logger.info(f"{filename} moved from UPLOADS to ARCHIVE")

        return render_template("results.html", value=test.as_dict())
    except ValidationError as error:
        app.logger.error(error)
        file_to_errors(filename)
        app.logger.info(f"{filename} moved from UPLOADS to ERROR")


@app.errorhandler(404)
def invalid_route(error):
    """
    Catch-all route for any unrecognized URLs

    Returns:
        Template: Custom 404 page
    """

    app.logger.error(error)
    return render_template('404.html')
