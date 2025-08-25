# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.passenger import Passenger
from schemas.schemas import passenger_schema, passengers_schema

# Define Blueprint for passenger
passenger_bp = Blueprint("passenger", __name__, url_prefix="/passengers")

# Routes
# GET
@passenger_bp.route("/")
def get_passengers():
    # Define GET statement
    stmt = db.select(Passenger)
    # Execute it
    passengers_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = passengers_schema.dump(passengers_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No passenger records found"}, 404
    
# GET /id
@passenger_bp.route("/<int:passenger_id>")
def get_a_passenger(passenger_id):
    # Define GET statment
    stmt = db.select(Passenger).where(Passenger.id == passenger_id)

    # Execute it
    passenger = db.session.scalar(stmt)

    # Error Handling
    if passenger:
        # Serialise
        data = passenger_schema.dump(passenger)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Passenger with id {passenger_id} not found."}, 404
    
# POST /
@passenger_bp.route("/", methods=["POST"])
def create_passenger():
    try:
        # GET info from the request body
        body_data = request.get_json()

        new_passenger = passenger_schema.load(
            body_data,
            session=db.session
        )

        # Add new passenger data to session
        db.session.add(new_passenger)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(passenger_schema.dump(new_passenger)), 201
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
        
# PUT/PATCH /id
@passenger_bp.route("/<int:passenger_id>", methods=["PUT", "PATCH"])
def update_passenger(passenger_id):
    try:
        # Define GET Statement
        stmt = db.select(Passenger).where(Passenger.id == passenger_id)

        # Execute statement
        passenger = db.session.scalar(stmt)

        if not passenger:
            return {"message": f"Passenger with id {passenger_id} does not exist/cannot be found."}, 404

        body_data = request.get_json()

        updated_passenger = passenger_schema.load(
            body_data,
            instance=passenger,
            partial=True,
            session=db.session
        )

        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(passenger_schema.dump(updated_passenger))
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
@passenger_bp.route("/<int:passenger_id>", methods=["DELETE"])
def delete_passenger(passenger_id):
        # Find the passenger with the passenger_id
    stmt = db.select(Passenger).where(Passenger.id == passenger_id)
    passenger = db.session.scalar(stmt)
    # if exists
    if passenger:
        # delete the passenger entry
        db.session.delete(passenger)
        db.session.commit()

        return {"message": f"Passenger '{passenger.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Passenger with id '{passenger_id}' does not exist"}, 404