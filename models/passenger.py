# Explain why this is imported
from init import db

# Explain the purpose of this class
class Passenger(db.Model):
    __tablename__ = "passengers"

    # Attributes of 'Passenger' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(100), nullable=False)

    # Foreign Key attribute
    plane_id = db.Column(db.Integer, db.ForeignKey("planes.id"))

    # Define relationship
    plane = db.relationship("Plane", back_populates="passengers")