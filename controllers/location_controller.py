# Installed imports
from flask import Blueprint, jsonify, request

# Created Module Imports
from init import db
from models.location import Location
from schemas.schemas import location_schema, locations_schema

# Define Blueprint for location
location_bp = Blueprint("location", __name__, url_prefix="/locations")

# Routes
# GET
@location_bp.route("/")
def get_locations():
    # Define GET statement
    stmt = db.select(Location)
    # Execute it
    locations_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = locations_schema.dump(locations_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No location records found"}, 404
    
# GET /id
@location_bp.route("/<int:location_id>")
def get_a_location(location_id):
    # Define GET statment
    stmt = db.select(Location).where(Location.id == location_id)

    # Execute it
    location = db.session.scalar(stmt)

    # Error Handling
    if location:
        # Serialise
        data = location_schema.dump(location)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Location with id {location_id} not found."}, 404