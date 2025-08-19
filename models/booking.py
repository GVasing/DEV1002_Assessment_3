# Explain why this is imported
from init import db

# Explain the purpose of this class
class Booking(db.Model):
    __tablename__ = "bookings"

    # Attributes of 'Booking' entity
    id = db.Column(db.Integer, primary_key=True)
    cabin_class = db.Column(db.String, nullable=False)
    checked_baggage = db.Column(db.Boolean, nullable=False)
    baggage_amount = db.Column(db.Float)
    seat_selected = db.Column(db.Boolean, nullable=False)
    meal_ordered = db.Column(db.String)
    ticket_price = db.Column(db.Float)