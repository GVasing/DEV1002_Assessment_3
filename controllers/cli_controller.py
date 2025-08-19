# Installed imports
from flask import Blueprint

# Created Module Imports
from init import db

# Define/Create a blueprint of 'app'
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_table():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("drop")
def drop_table():
    db.drop_all()
    print("Tables dropped.")