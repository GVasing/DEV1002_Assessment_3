# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.airport import Airport
from schemas.schemas import airport_schema, airports_schema

# Define Blueprint for airport
airport_bp = Blueprint("airport", __name__, url_prefix="/airports")

# Routes
# GET
@airport_bp.route("/")
def get_airports():
    # Define GET statement
    stmt = db.select(Airport)
    # Execute it
    airports_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = airports_schema.dump(airports_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No airport records found"}, 404
    
# GET /id
@airport_bp.route("/<int:airport_id>")
def get_a_airport(airport_id):
    # Define GET statment
    stmt = db.select(Airport).where(Airport.id == airport_id)

    # Execute it
    airport = db.session.scalar(stmt)

    # Error Handling
    if airport:
        # Serialise
        data = airport_schema.dump(airport)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Airport with id {airport_id} not found."}, 404
    
# POST /
@airport_bp.route("/", methods=["POST"])
def create_a_airport():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Airport Object from Airport class/model with body response data
        new_airport = Airport(
            name=body_data.get("name"),
            total_terminal_amount=body_data.get("total_terminal_amount"),
            international_terminal_amount=body_data.get("international_terminal_amount"),
            domestic_terminal_amount=body_data.get("domestic_terminal_amount"),
            number_of_runways=body_data.get("number_of_runways"),
            location_id=body_data.get("location_id")
        )
        # Add new airport data to session
        db.session.add(new_airport)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(airport_schema.dump(new_airport)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Airline name must be unique"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@airport_bp.route("/<int:airport_id>", methods=["PUT", "PATCH"])
def update_airport(airport_id):
    # Define GET Statement
    stmt = db.select(Airport).where(Airport.id == airport_id)

    # Execute statement
    airport = db.session.scalar(stmt)

    # If/Elif/Else Conditions
    if airport:
        # Retrieve 'airport' data
        body_data = request.get_json()
        # Specify changes
        airport.name = body_data.get("name") or airport.name
        airport.total_terminal_amount = body_data.get("total_terminal_amount") or airport.total_terminal_amount
        airport.international_terminal_amount = body_data.get("international_terminal_amount") or airport.international_terminal_amount
        airport.domestic_terminal_amount = body_data.get("domestic_terminal_amount") or airport.domestic_terminal_amount
        airport.number_of_runways = body_data.get("number_of_runways") or airport.number_of_runways
        airport.location_id = body_data.get("location_id") or airport.location_id
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(airport_schema.dump(airport))
    else:
        return {"message": f"Airport with id {airport_id} does not exist/cannot be found."}, 404

# DELETE /id
@airport_bp.route("/<int:airport_id>", methods=["DELETE"])
def delete_a_airport(airport_id):
        # Find the airport with the airport_id
    stmt = db.select(Airport).where(Airport.id == airport_id)
    airport = db.session.scalar(stmt)
    # if exists
    if airport:
        # delete the airport entry
        db.session.delete(airport)
        db.session.commit()

        return {"message": f"'{airport.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Airport with id '{airport_id}' does not exist"}, 404