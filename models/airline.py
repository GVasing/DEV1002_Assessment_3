# Explain why this is imported
from init import db

# Explain the purpose of this class
class Airline(db.Model):
    __tablename__ = "airlines"

    # Attributes of 'Airline' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    airline_name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    fleet_size = db.Column(db.Integer)
    number_of_destinations = db.Column(db.Integer)

    # Define Relationship
    flights = db.relationship("Flight", back_populates="airline", cascade = "all, delete")