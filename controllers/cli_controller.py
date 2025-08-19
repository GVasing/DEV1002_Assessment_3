# Installed imports
from flask import Blueprint

# Created Module Imports
from init import db
from models.location import Location

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

@db_commands.cli.command("seed")
def seed_tables():
    # Create an instance of the Model
    locations = [
        Location(
            city_name="Melbourne",
            country_name="Australia"
        ), 
        Location(
            city_name="Sydney",
            country_name="Australia"
        )
    ]
    # Add to session
    db.session.add_all(locations)

    # Commit session
    db.session.commit()
    print("Tables seeded.")