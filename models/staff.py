# Explain why this is imported
from init import db

# Explain the purpose of this class
class Staff(db.Model):
    __tablename__ = "staff"

    # Attributes of 'Staff' entity
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    employment = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    salary = db.Column(db.Float)
    years_worked = db.Column(db.Float)