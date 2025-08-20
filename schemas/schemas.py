# Installed imports
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, And, Regexp, Range, OneOf
from marshmallow import validates, ValidationError, fields, validate

# Created Module Imports
from models.airline import Airline
from models.airport import Airport
from models.booking import Booking
from models.flight import Flight
from models.location import Location
from models.passenger import Passenger
from models.plane import Plane
from models.staff import Staff


class AirlineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Airline
        load_instance = True
        include_relationships = True

class AirportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        load_instance = True
        include_relationships = True

class BookingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_relationships = True

class FlightSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        load_instance = True
        include_relationships = True

class LocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        include_relationships = True

class PassengerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Passenger
        load_instance = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "age", "gender", "plane")
    
    # plane = fields.Nested("PlaneSchema", only=("id", "manufacturer", "model"))

class PlaneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plane
        load_instance = True
        include_relationships = True
        fields = ("id", "manufacturer", "model", "range", "passenger_capacity", "fuel_capacity")

    manufacturer = auto_field(validate=OneOf(["Boeing", "Airbus", "Embraer", "Bombardier", "Cessna", "Pilatus", "ATR", "De Havilland Canada"], error="Manufacturer not within the available options"))

class StaffSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Staff
        load_instance = True
        include_relationships = True

# Airline Schema for converting a single entry
airline_schema = AirlineSchema()
# Airline Schema for converting multiple entries
airlines_schema = AirlineSchema(many=True)

# Airport Schema for converting a single entry
airport_schema = AirportSchema()
# Airport Schema for converting multiple entries
airports_schema = AirportSchema(many=True)

# Booking Schema for converting a single entry
booking_schema = BookingSchema()
# Booking Schema for converting multiple entries
bookings_schema = BookingSchema(many=True)

# Flight Schema for converting a single entry
flight_schema = FlightSchema()
# Flight Schema for converting multiple entries
flights_schema = FlightSchema(many=True)

# Location Schema for converting a single entry
location_schema = LocationSchema()
# Location Schema for converting multiple entries
locations_schema = LocationSchema(many=True)

# Passenger Schema for converting a single entry
passenger_schema = PassengerSchema()
# Passenger Schema for converting multiple entries
passengers_schema = PassengerSchema(many=True)

# Plane Schema for converting a single entry
plane_schema = PlaneSchema()
# Plane Schema for converting multiple entries
planes_schema = PlaneSchema(many=True)

# Staff Schema for converting a single entry
staff_schema = StaffSchema()
# Staff Schema for converting multiple entries
staffs_schema = StaffSchema(many=True)