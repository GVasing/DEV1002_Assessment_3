# Explain why this is imported
from init import db

# Explain the purpose of this class
class Airline(db.Model):
    __tablename__ = "airlines"

    # Attributes of 'Airline' entity
    id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String, nullable=False, unique=True)
    origin = db.Column(db.String, nullable=False)
    fleet_size = db.Column(db.Integer)
    number_of_destinations = db.Column(db.Integer)