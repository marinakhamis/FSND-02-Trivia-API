import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Feel free to edit this when you work on your own database
database_info = {
    "database_name": "trivia",
    "database_name_test": "trivia_test",
    "user_name": "postgres",
    "password": "8246",
    "port": "localhost:5432"
}
