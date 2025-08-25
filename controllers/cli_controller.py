# Built-in imports
from datetime import time, date

# Installed imports
from flask import Blueprint
from sqlalchemy import text

# Created Module Imports
from init import db
from models.location import Location
from models.airline import Airline
from models.plane import Plane
from models.staff import Staff
from models.passenger import Passenger
from models.flight import Flight
from models.airport import Airport
from models.booking import Booking

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
        ),
        Location(
            city_name="La Paz",
            country_name="Bolivia"
        ),
        Location(
            city_name="La Paz",
            country_name="Mexico"
        ),
        Location(
            city_name="New York City",
            country_name="United States of America"
        ),
        Location(
            city_name="Vancouver",
            country_name="Canada"
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
        ),
        Airline(
            airline_name="Emirates",
            origin="United Arab Emirates (UAE)",
            fleet_size=270,
            number_of_destinations=133
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
        ),
        Plane(
            manufacturer="Airbus",
            model="A380-800",
            passenger_capacity= 525,
            fuel_capacity= 320000
        )
    ]

    # Add to session
    db.session.add_all(planes)
    
    # Commit session here prior to creation of dependenent tables to generate foreign keys for them.
    db.session.commit()

    # Create instance(s) of Passenger
    passengers = [
        Passenger(
            name="John Smith",
            age= 55,
            gender="Male",
            plane_id=planes[0].id
        ),
        Passenger(
            name="Jane Doe",
            age= 46,
            gender="Female",
            plane_id=planes[1].id
        ),
        Passenger(
            name="Tom Chance",
            age= 32,
            gender="Male",
            plane_id=planes[0].id
        ),
        Passenger(
            name="Jess Smith",
            age= 54,
            gender="Female",
            plane_id=planes[1].id
        )
    ]

    # Add to session
    db.session.add_all(passengers)

    # Create instance(s) of Flight
    flights = [
        Flight(
            departure_point="Melbourne",
            destination="Sydney",
            flight_code="QF446",
            departure_time= time(13, 30),
            arrival_time= time(14, 55),
            departure_date= date(2025, 8, 20),  # date(year, month, day)
            flight_duration= 95,
            airline_id=airlines[0].id
        ),
        Flight(
            departure_point="Sydney",
            destination="Brisbane",
            flight_code="QF526",
            departure_time= time(13, 55),
            arrival_time= time(15, 25),
            departure_date= date(2025, 8, 20),
            flight_duration= 93,
            airline_id=airlines[0].id
        ),
        Flight(
            departure_point="Sydney",
            destination="Perth",
            flight_code="QF641",
            departure_time= time(6, 52),
            arrival_time= time(10, 8),
            departure_date= date(2025, 8, 21),
            flight_duration= 316,
            airline_id=airlines[0].id
        )
    ]

    # Add to session
    db.session.add_all(flights)

    # Create instance(s) of Aiport
    airports = [
        Airport(
            name="Melbourne Aiport",
            total_terminal_amount= 4,
            international_terminal_amount= 2,
            domestic_terminal_amount= 3,
            number_of_runways= 2,
            location_id=locations[0].id

        ),
        Airport(
            name="Sydney Kingsford Smith Airport",
            total_terminal_amount= 3,
            international_terminal_amount= 1,
            domestic_terminal_amount= 2,
            number_of_runways= 3,
            location_id=locations[1].id
        ),
        Airport(
            name="Vancouver International Airport",
            total_terminal_amount= 3,
            international_terminal_amount= 1,
            domestic_terminal_amount= 2,
            number_of_runways= 3,
            location_id=locations[5].id
        )
    ]

    # Add to session
    db.session.add_all(airports)

    # Commit session here prior to creation of dependenent tables to generate foreign keys for them.
    db.session.commit()

    # Create an instance(s) of Staff
    staffs = [
        Staff(
            name="Jeanie Coleman",
            age= 31,
            gender= "Female",
            employment= "Full-Time",
            position= "Passenger Service Agent",
            salary= 70000,
            years_worked= 6,
            airport_id=airports[0].id 
        ),
        Staff(
            name="Felix Morrison",
            age= 25,
            gender= "Male",
            employment= "Part-Time",
            position= "Baggage Handler",
            salary= 38000,
            years_worked= 3,
            airport_id=airports[1].id
        ),
        Staff(
            name="Stan Rodriguez",
            age= 47,
            gender= "Male",
            employment= "Full-Time",
            position= "Security",
            salary= 60000,
            years_worked= 12,
            airport_id=airports[0].id
        ),
        Staff(
            name="Jess Bauer",
            age= 32,
            gender= "Male",
            employment= "Part-Time",
            position= "Cabin Crew",
            salary= 50000,
            years_worked= 4,
            airport_id=airports[1].id
        )
    ]

    # Add to session
    db.session.add_all(staffs)

    # Commit here to generate multiple forgein keys for junction table (Booking)
    db.session.commit()

    # Create instance(s) of Booking
    bookings = [
        Booking(
            cabin_class="Economy",
            checked_baggage= False,
            baggage_amount= 0,
            seat_selected= False,
            meal_ordered=None,
            ticket_price= 372,
            airport_id=airports[0].id,
            flight_id=flights[0].id,
            passenger_id=passengers[0].id,
        ),
        Booking(
            cabin_class="Economy",
            checked_baggage= True,
            baggage_amount= 25.5,
            seat_selected= False,
            meal_ordered="Chicken w/ Rice",
            ticket_price= 400.50,
            airport_id=airports[1].id,
            flight_id=flights[1].id,
            passenger_id=passengers[1].id,
        ),
        Booking(
            cabin_class="Business Class",
            checked_baggage= False,
            baggage_amount= 0,
            seat_selected= False,
            meal_ordered="Beef Pasta Ragu",
            ticket_price= 1113.75,
            airport_id=airports[0].id,
            flight_id=flights[0].id,
            passenger_id=passengers[3].id,
        )
    ]

    # Add to session
    db.session.add_all(bookings)

    # Commit session
    db.session.commit()
    print("Tables seeded.")