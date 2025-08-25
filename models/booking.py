# Explain why this is imported
from init import db

# Explain the purpose of this class
class Booking(db.Model):
    __tablename__ = "bookings"

    # Attributes of 'Booking' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    cabin_class = db.Column(db.String(100), nullable=False)
    checked_baggage = db.Column(db.Boolean, nullable=False)
    baggage_amount = db.Column(db.Float)
    seat_selected = db.Column(db.Boolean, nullable=False)
    meal_ordered = db.Column(db.String(100))
    ticket_price = db.Column(db.Float)

    # Foreign Key attributes
    airport_id = db.Column(db.Integer, db.ForeignKey("airports.id"), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey("passengers.id"), nullable=False)

    # Define relationships
    airport = db.relationship("Airport", back_populates="bookings")
    flight = db.relationship("Flight", back_populates="bookings")
    passenger = db.relationship("Passenger", back_populates="bookings")