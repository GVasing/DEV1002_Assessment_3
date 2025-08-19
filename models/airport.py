# Explain why this is imported
from init import db

# Explain the purpose of this class
class Airport(db.Model):
    __tablename__ = "airports"

    # Attributes of 'Airport' entity
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    total_terminal_amount = db.Column(db.Integer)
    international_terminal_amount = db.Column(db.Integer)
    domestic_terminal_amount = db.Column(db.Integer)
    number_of_runways = db.Column(db.Integer)