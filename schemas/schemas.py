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
        ordered = True
        fields = ("id", "airline_name", "origin", "fleet_size", "number_of_destinations")

class AirportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "total_terminal_amount", "international_terminal_amount", "domestic_terminal_amount", "number_of_runways", "location_id", "location")

    # staff = fields.Nested("StaffSchema", only=("airline_name",))
    location = fields.Nested("LocationSchema", only=("city_name", "country_name"))

    @validates("international_terminal_amount")
    def validates_international_terminals(self, value):
        if value is None:
            raise ValidationError("International terminal amount is required")
        
        if value < 0:
            raise ValidationError("Must be 0 or greater.")

class BookingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "cabin_class", "checked_baggage", "baggage_amount", "seat_selected", "meal_ordered", "ticket_price", "airport_id", "flight_id", "passenger_id", "airport", "flight", "passenger")

    airport = fields.Nested("AirportSchema", only=("name", "location"))
    flight = fields.Nested("FlightSchema", only=("destination",))
    passenger = fields.Nested("PassengerSchema", only=("name", ))

class FlightSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "departure_point", "destination", "flight_code", "departure_time", "arrival_time", "departure_date", "flight_duration", "airline_id", "airline")

    airline = fields.Nested("AirlineSchema", only=("airline_name",))

class LocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        include_relationships = True
        fields = ("id", "city_name", "country_name")

    @validates("city_name")
    def validates_city_name(self, city_name, data_key):
        if not city_name:
            raise ValidationError("City name is required.")
        if len(city_name) < 2:
            print("City name is too short")
            raise ValidationError("City name is too short")
    
    @validates("country_name")
    def validates_country_name(self, country_name, data_key):
        if not country_name:
            raise ValidationError("Country name is required.")
        if len(country_name) < 2:
            print("Country name is too short")
            raise ValidationError("Country name is too short")

    # airport = fields.Nested("AirportSchema", only=("name",))

class PassengerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Passenger
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "age", "gender", "plane_id", "plane")
    
    plane = fields.Nested("PlaneSchema", only=("id", "manufacturer", "model"))

class PlaneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plane
        load_instance = True
        include_relationships = True
        ordered = True
        fields = ("id", "manufacturer", "model", "range", "passenger_capacity", "fuel_capacity")

    manufacturer = auto_field(validate=OneOf(["Boeing", "Airbus", "Embraer", "Bombardier", "Cessna", "Pilatus", "ATR", "De Havilland Canada"], error="Manufacturer not within the available options"))

    @validates("model")
    def validates_range(self, model, data_key):
        if not model:
            raise ValidationError("Non null value must not be empty")

class StaffSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Staff
        load_instance = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "age", "gender", "employment", "position", "salary", "years_worked")

    # airport = fields.Nested("AirportSchema", only=("name",))

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