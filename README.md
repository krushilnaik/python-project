# Smoothstack Python Course Final Project

## Table of Contents
- [Smoothstack Python Course Final Project](#smoothstack-python-course-final-project)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Setup](#setup)


## Description 

Rewriting ASCII Generator using Flask because it turns out there's less boiletplate code, which == less files to submit 👍

The final project for my university Python class, this is a simple webpage powered by ~~Beaker~~ Flask.

The frontend is a simple form with a text field and a submit button, the latter of which calls an API endpoint to display an ASCII art representation of what the user (probably you) typed. Just like ✨ magic ✨

## Setup

NOTE: this assumes you already have MySQL installed and running.

To install the Python dependencies:
```
pip install -r requirements.txt
```

To run the Flask app:
```
flask --app app run
```

Alternatively, if you have Docker, you can just run:

```
docker compose -f "docker-compose.yml" up -d --build
```

This will set up MySQL for you, as well as phpMyAdmin for a GUI that you can view the database with.
