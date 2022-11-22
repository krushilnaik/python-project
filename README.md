# Smoothstack Python Course Final Project

# Table of Contents
- [Smoothstack Python Course Final Project](#smoothstack-python-course-final-project)
- [Table of Contents](#table-of-contents)
- [Setup](#setup)
  - [With MySQL and Python:](#with-mysql-and-python)
  - [With Docker:](#with-docker)

# Setup

## With MySQL and Python:

To install the Python dependencies:
```
pip install -r requirements.txt
```

To run the Flask app:
```
flask --app app run
```

The app will now be accessible on http://localhost:5000.

## With Docker:

```
docker compose -f "docker-compose.yml" up -d --build
```

This will set up MySQL for you, as well as phpMyAdmin for a GUI that you can view the database with (on http://localhost:8080).
