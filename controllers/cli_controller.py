# Installed imports
from flask import Blueprint

# Created Module Imports
from init import db
from models.location import Location
from models.airline import Airline
from models.plane import Plane

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
    # Create an instance(s) of Location
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

    # Create an instance(s) of Airline
    airlines = [
        Airline(
            airline_name="Qantas",
            origin="Australia",
            fleet_size=308,
            number_of_destinations=102
        ),
        Airline(
            airline_name="Singapore Airlines",
            origin="Singapore",
            fleet_size=157,
            number_of_destinations=79
        )
    ]

    # Add to session
    db.session.add_all(airlines)

    # Create an instance(s) of Plane
    planes = [
        Plane(
            manufacturer="Boeing",
            model="747-400",
            range= 13450,
            passenger_capacity= 524,
            fuel_capacity= 216850
        ),
        Plane(
            manufacturer="Airbus",
            model="A330-300",
            range= 11300,
            passenger_capacity= 290,
            fuel_capacity= 139090
        )
    ]

    # Add to session
    db.session.add_all(planes)

    # Commit session
    db.session.commit()
    print("Tables seeded.")