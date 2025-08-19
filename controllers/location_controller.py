# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

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
    
# POST /
@location_bp.route("/", methods=["POST"])
def create_a_location():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Location Object from Location class/model with body response data
        new_location = Location(
            city_name=body_data.get("city_name"),
            country_name=body_data.get("country_name"),
        )
        # Add new location data to session
        db.session.add(new_location)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(location_schema.dump(new_location)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@location_bp.route("/<int:location_id>", methods=["PUT", "PATCH"])
def update_location(location_id):
    # Define GET Statement
    stmt = db.select(Location).where(Location.id == location_id)

    # Execute statement
    location = db.session.scalar(stmt)

    # If/Elif/Else Conditions
    if location:
        # Retrieve 'location' data
        body_data = request.get_json()
        # Specify changes
        location.city_name = body_data.get("city_name") or location.city_name
        location.country_name = body_data.get("country_name") or location.country_name
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(location_schema.dump(location))
    else:
        return {"message": f"Location with id {location_id} does not exist/cannot be found."}, 404

# DELETE /id
@location_bp.route("/<int:location_id>", methods=["DELETE"])
def delete_a_location(location_id):
        # Find the location with the location_id
    stmt = db.select(Location).where(Location.id == location_id)
    location = db.session.scalar(stmt)
    # if exists
    if location:
        # delete the location entry
        db.session.delete(location)
        db.session.commit()

        return {"message": f"Location '{location.city_name}, {location.country_name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Location with id '{location_id}' does not exist"}, 404