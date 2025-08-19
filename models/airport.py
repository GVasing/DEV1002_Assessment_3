# Explain why this is imported
from init import db

# Explain the purpose of this class
class Airport(db.Model):
    __tablename__ = "airports"

    # Attributes of 'Airport' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    name = db.Column(db.String(100), nullable=False, unique=True)
    total_terminal_amount = db.Column(db.Integer)
    international_terminal_amount = db.Column(db.Integer)
    domestic_terminal_amount = db.Column(db.Integer)
    number_of_runways = db.Column(db.Integer)