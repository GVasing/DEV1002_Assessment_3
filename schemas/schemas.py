# Installed imports
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import OneOf
from marshmallow import validates, ValidationError, fields

# Created Module Imports
from models.plane import Plane
from models.location import Location
from models.airline import Airline
from models.airport import Airport
from models.staff import Staff
from models.flight import Flight
from models.passenger import Passenger
from models.booking import Booking


class AirlineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Airline
        load_instance = True
        include_relationships = True
        ordered = True
        fields = ("id", "airline_name", "origin", "fleet_size", "number_of_destinations")

    @validates("airline_name")
    def validates_airline_name(self, airline_name, data_key):
        if len(airline_name) < 2:
            raise ValidationError("Airline name is required.")
    
    @validates("origin")
    def validates_range(self, origin, data_key):
        if len(origin) < 2:
            raise ValidationError("Origin is required.")
        
    @validates("fleet_size")
    def validates_fleet_size(self, fleet_size, data_key):
        if fleet_size <= 0:
            raise ValueError
        
    @validates("number_of_destinations")
    def validates_number_of_destinations(self, number_of_destinations, data_key):
        if number_of_destinations <= 0:
            raise ValidationError("Number of destinations cannot be zero or less.")

class AirportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "total_terminal_amount", "international_terminal_amount", "domestic_terminal_amount", "number_of_runways", "location_id", "location")

    location = fields.Nested("LocationSchema", only=("city_name", "country_name"))

    @validates("name")
    def validates_name(self, name, data_key):
        if not name:
            raise ValidationError("Airport name must not be empty")
        if len(name) < 1:
            raise ValidationError("Airport name must not be empty")
        
    @validates("total_terminal_amount")
    def validates_total_terminal_amount(self, total_terminal_amount, data_key):
        if not total_terminal_amount:
            raise ValidationError("Enter a positive or valid integer, or null.")
        if total_terminal_amount <= 0:
            raise ValueError("Value must not be zero or less.")
    
    @validates("international_terminal_amount")
    def validates_international_terminals(self, international_terminal_amount, data_key):
        if international_terminal_amount == 0:
            pass
        elif type(international_terminal_amount) != int:
            raise ValidationError("Enter a valid integer or null.")
        
    @validates("domestic_terminal_amount")
    def validates_domestic_terminal_amount(self, domestic_terminal_amount, data_key):
        if not domestic_terminal_amount:
            raise ValidationError("Enter a positive integer or null.")
        
    @validates("number_of_runways")
    def validates_number_of_runways(self, number_of_runways, data_key):
        if number_of_runways <= 0:
            raise ValueError("Value must not be zero or less. For none, enter null.")

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

    cabin_class = auto_field(validate=OneOf(["Economy", "Premium Economy", "Business", "Business Class", "First Class"], error="cabin class not recognised"))

class FlightSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "departure_point", "destination", "flight_code", "departure_time", "arrival_time", "departure_date", "flight_duration", "airline_id", "airline")

    airline = fields.Nested("AirlineSchema", only=("airline_name",))

    @validates("departure_point")
    def validates_departure_point(self, departure_point, data_key):
        if not departure_point:
            raise ValidationError("Departure Point non null value must not be empty")
        
    @validates("destination")
    def validates_destination(self, destination, data_key):
        if not destination:
            raise ValidationError("Destination non null value must not be empty")\
            
    @validates("flight_code")
    def validates_flight_code(self, flight_code, data_key):
        if not flight_code:
            raise ValidationError("Flight Code non null value must not be empty")

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

class PassengerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Passenger
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "age", "gender", "plane_id", "plane")
    
    plane = fields.Nested("PlaneSchema", only=("id", "manufacturer", "model"))

    @validates("name")
    def validates_passenger_name(self, name, data_key):
        if not name:
            raise ValidationError("Name must not be empty string.")
    
    gender = auto_field(validate=OneOf(["Male", "Female", "Non-Binary", "Other"], error="Please select from: 'Male', 'Female', 'Non-Binary', 'Other'"))

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
            raise ValidationError("Model must not be empty")
        
    @validates("passenger_capacity")
    def validates_passenger_capacity(self, passenger_capacity, data_key):
        if passenger_capacity < 1:
            raise ValueError
        
    @validates("fuel_capacity")
    def validates_fuel_capacity(self, fuel_capacity, data_key):
        if fuel_capacity < 1:
            raise ValueError

class StaffSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Staff
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "age", "gender", "employment", "position", "salary", "years_worked", "airport_id", "airport")

    airport = fields.Nested("AirportSchema", only=("name",))

    @validates("name")
    def validates_staff_member_name(self, name, data_key):
        if not name:
            raise ValidationError("Name non null value must not be empty") 
        
    employment = auto_field(validate=OneOf(["Full-Time", "Part-Time", "Casual", "Contract"], error="Employment options must be one of the following:'Full-Time', 'Part-Time', 'Casual', 'Contract'"))

    gender = auto_field(validate=OneOf(["Male", "Female", "Non-Binary", "Other"], error="Please select from: 'Male', 'Female', 'Non-Binary', 'Other'"))

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