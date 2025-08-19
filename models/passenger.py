# Explain why this is imported
from init import db

# Explain the purpose of this class
class Passenger(db.Model):
    __tablename__ = "passengers"

    # Attributes of 'Passenger' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)