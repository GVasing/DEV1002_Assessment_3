# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.flight import Flight
from schemas.schemas import flight_schema, flights_schema

# Define Blueprint for flight
flight_bp = Blueprint("flight", __name__, url_prefix="/flights")

# Routes
# GET
@flight_bp.route("/")
def get_flights():
    # Define GET statement
    stmt = db.select(Flight)
    # Execute it
    flights_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = flights_schema.dump(flights_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No flight records found"}, 404
    
# GET /id
@flight_bp.route("/<int:flight_id>")
def get_a_flight(flight_id):
    # Define GET statment
    stmt = db.select(Flight).where(Flight.id == flight_id)

    # Execute it
    flight = db.session.scalar(stmt)

    # Error Handling
    if flight:
        # Serialise
        data = flight_schema.dump(flight)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Flight with id {flight_id} not found."}, 404
    
# POST /
@flight_bp.route("/", methods=["POST"])
def create_flight():
    try:
        # GET info from the request body
        body_data = request.get_json()

        new_flight = flight_schema.load(
            body_data,
            session=db.session
        )
        # Add new flight data to session
        db.session.add(new_flight)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(flight_schema.dump(new_flight)), 201
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"message": "Invalid format given or no data provided."}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Flight code must be unique"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@flight_bp.route("/<int:flight_id>", methods=["PUT", "PATCH"])
def update_flight(flight_id):
    try:
        # Define GET Statement
        stmt = db.select(Flight).where(Flight.id == flight_id)

        # Execute statement
        flight = db.session.scalar(stmt)

        if not flight:
            return {"message": f"Flight with id {flight_id} does not exist/cannot be found."}, 404

        body_data = request.get_json()

        updated_flight = flight_schema.load(
            body_data,
            instance=flight,
            partial=True,
            session=db.session
        )

        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(flight_schema.dump(updated_flight))
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"message": "Invalid format given or no data provided."}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        elif err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
            

# DELETE /id
@flight_bp.route("/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
        # Find the flight with the flight_id
    stmt = db.select(Flight).where(Flight.id == flight_id)
    flight = db.session.scalar(stmt)
    # if exists
    if flight:
        # delete the flight entry
        db.session.delete(flight)
        db.session.commit()

        return {"message": f"Flight '{flight.flight_code}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Flight with id '{flight_id}' does not exist"}, 404