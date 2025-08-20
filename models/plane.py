# Explain why this is imported
from init import db

# Explain the purpose of this class
class Plane(db.Model):
    __tablename__ = "planes"

    # Attributes of 'Plane' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False, unique=True)
    range = db.Column(db.Float)
    passenger_capacity = db.Column(db.Integer, nullable=False)
    fuel_capacity = db.Column(db.Integer, nullable=False)

    # Define Relationship
    passengers = db.relationship("Passenger", back_populates="plane")