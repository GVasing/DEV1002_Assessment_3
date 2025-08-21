# Explain why this is imported
from init import db

# Explain the purpose of this class
class Flight(db.Model):
    __tablename__ = "flights"

    # Attributes of 'Flight' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    departure_point = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    flight_code = db.Column(db.String(100), nullable=False, unique=True)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    flight_duration = db.Column(db.Float, nullable=False)

    # Foreign Key attribute
    airline_id = db.Column(db.Integer, db.ForeignKey("airlines.id", ondelete="CASCADE"), nullable=False)

    # Define relationship
    airline = db.relationship("Airline", back_populates="flights")
    bookings = db.relationship("Booking", back_populates="flight")