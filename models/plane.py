# Explain why this is imported
from init import db

# Explain the purpose of this class
class Plane(db.Model):
    __tablename__ = "planes"

    # Attributes of 'Plane' entity
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False, unique=True)
    range = db.Column(db.Float)
    passenger_capacity = db.Column(db.Integer, nullable=False)
    fuel_capacity = db.Column(db.Integer, nullable=False)