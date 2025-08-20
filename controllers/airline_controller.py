# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.airline import Airline
from schemas.schemas import airline_schema, airlines_schema

# Define Blueprint for airline
airline_bp = Blueprint("airline", __name__, url_prefix="/airlines")

# Routes
# GET
@airline_bp.route("/")
def get_airlines():
    # Define GET statement
    stmt = db.select(Airline)
    # Execute it
    airlines_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = airlines_schema.dump(airlines_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No airline records found"}, 404
    
# GET /id
@airline_bp.route("/<int:airline_id>")
def get_a_airline(airline_id):
    # Define GET statment
    stmt = db.select(Airline).where(Airline.id == airline_id)

    # Execute it
    airline = db.session.scalar(stmt)

    # Error Handling
    if airline:
        # Serialise
        data = airline_schema.dump(airline)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Airline with id {airline_id} not found."}, 404
    
# POST /
@airline_bp.route("/", methods=["POST"])
def create_a_airline():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Airline Object from Airline class/model with body response data
        new_airline = Airline(
            airline_name=body_data.get("airline_name"),
            origin=body_data.get("origin"),
            fleet_size=body_data.get("fleet_size"),
            number_of_destinations=body_data.get("number_of_destinations")
        )
        # Add new airline data to session
        db.session.add(new_airline)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(airline_schema.dump(new_airline)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Airline name must be unique"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@airline_bp.route("/<int:airline_id>", methods=["PUT", "PATCH"])
def update_airline(airline_id):
    # Define GET Statement
    stmt = db.select(Airline).where(Airline.id == airline_id)

    # Execute statement
    airline = db.session.scalar(stmt)

    # If/Elif/Else Conditions
    if airline:
        # Retrieve 'airline' data
        body_data = request.get_json()
        # Specify changes
        airline.airline_name = body_data.get("airline_name") or airline.airline_name
        airline.origin = body_data.get("origin") or airline.origin
        airline.fleet_size = body_data.get("fleet_size") or airline.fleet_size
        airline.number_of_destinations = body_data.get("number_of_destinations") or airline.number_of_destinations
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(airline_schema.dump(airline))
    else:
        return {"message": f"Airline with id {airline_id} does not exist/cannot be found."}, 404

# DELETE /id
@airline_bp.route("/<int:airline_id>", methods=["DELETE"])
def delete_a_airline(airline_id):
        # Find the airline with the airline_id
    stmt = db.select(Airline).where(Airline.id == airline_id)
    airline = db.session.scalar(stmt)
    # if exists
    if airline:
        # delete the airline entry
        db.session.delete(airline)
        db.session.commit()

        return {"message": f"Airline '{airline.airline_name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Airline with id '{airline_id}' does not exist"}, 404