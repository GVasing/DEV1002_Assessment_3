# Explain why this is imported
from init import db

# Explain the purpose of this class
class Staff(db.Model):
    __tablename__ = "staff"

    # Attributes of 'Staff' entity

    # Primary Key attribute
    id = db.Column(db.Integer, primary_key=True)

    # Non-Key attributes
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    employment = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float)
    years_worked = db.Column(db.Float)

    # Foreign Key attribute
    airport_id = db.Column(db.Integer, db.ForeignKey("airports.id"), nullable=False)

    # Define Relationship
    airports = db.relationship("Airport", back_populates="staff")