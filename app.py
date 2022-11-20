"""
Smoothstack Evaluation Week Final Project
"""

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from openpyxl import load_workbook
from models import db
from pathlib import Path
from models.Summary import Summary, SummaryValidator
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root@database/smoothstack"
app.secret_key = "55e36cb88d9251f1bd812ec5242e5ead"

db.init_app(app)

with app.app_context():
    db.create_all()

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

SUMMARY_SHEET = "Summary Rolling MoM"
VOC_SHEET = "VOC Rolling MoM"
VERBATIM_SHEET = "Monthly Verbatim Statements"

VALID_SHEETS = set([
    "Summary Rolling MoM",
    "VOC Rolling MoM",
    "Monthly Verbatim Statements"
])

UPLOADS = Path('./uploads')
ARCHIVE = Path('./archive')
ERROR = Path('./error')

# create the above directories if they don't exist
for dir in [UPLOADS, ARCHIVE, ERROR]:
    dir.mkdir(parents=True, exist_ok=True)


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

    file = request.files["file"]

    if not file.filename:
        flash("No file uploaded")
        return redirect(url_for('index'))

    # cleanse file path of crazy characters
    filename = secure_filename(file.filename)

    # check if file has already been parsed
    with open('processed.lst', 'r+') as processed:
        if filename in processed.read():
            flash(f"{filename} has already been processed")
            return redirect(url_for('index'))
        else:
            processed.write(filename + "\n")

    file.save(UPLOADS / filename)

    # parse file with openpyxl
    wb = load_workbook(UPLOADS / filename, data_only=True)

    # check if all three tabs are present (if not, move to ERROR)
    if len(wb.sheetnames) != 3 or set(wb.sheetnames) != VALID_SHEETS:
        flash("Error: malformed speadsheet")
        os.replace(UPLOADS / filename, ERROR / filename)
        return redirect(url_for("index"))

    SHEET = wb[SUMMARY_SHEET]
    COLUMNS = ["A", "B", "C", "D", "E", "F"]

    try:
        # A well formed sheet has relavent data in rows 2 to 14 (for the 12 months)
        for r in range(2, 14):
            values = [SHEET[f"{c}{r}"].value for c in COLUMNS]

            SummaryValidator(
                time_period=values[0],
                calls_offered=values[1],
                abandoned_after_30=values[2],
                fcr=values[3],
                dsat=values[4],
                csat=values[5]
            )

            # write validated data for that month and year to mysql
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
        parts = filename.split("_")[-2:]

        month = MONTHS[parts[0].lower()[:3]]
        year = parts[1][:4]

        # fetch the first entry found that was recorded on the month in question
        # (between the 1st and 31st of that month)
        test = Summary.query.filter(Summary.time_period.between(
            f'{year}-{month}-01', f'{year}-{month}-31')
        ).first()

        # move file to ARCHIVE
        os.replace(UPLOADS / filename, ARCHIVE / filename)

        return render_template("results.html", value=test.as_dict())
    except:
        os.replace(UPLOADS / filename, ERROR / filename)


@app.errorhandler(404)
def invalid_route(e):
    """
    Catch-all route for any unrecognized URLs

    Returns:
        Template: Custom 404 page
    """
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    """
    Custom page to render in the event of a server-side error

    Returns:
        Template: Custom 500 page
    """
    return render_template('500.html')
