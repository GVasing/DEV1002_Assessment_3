# Explain why this is imported
from init import db

# Explain the purpose of this class
class Location(db.Model):
    __tablename__ = "locations"

    # Attributes of 'Location' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    city_name = db.Column(db.String(100), nullable=False)
    country_name = db.Column(db.String(100), nullable=False)

    # Define Relationship
    airports = db.relationship("Airport", back_populates="location", cascade = "all, delete")