# Explain why this is imported
from init import db

# Explain the purpose of this class
class Flight(db.Model):
    __tablename__ = "flights"

    # Attributes of 'Flight' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    departure_point = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    flight_code = db.Column(db.String, nullable=False, unique=True)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    flight_duration = db.Column(db.Float, nullable=False)