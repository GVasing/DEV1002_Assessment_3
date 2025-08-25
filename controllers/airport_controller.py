# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
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
def get_an_airport(airport_id):
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
def create_airport():
    try:
        # GET info from the request body
        body_data = request.get_json()

        new_airport = airport_schema.load(
            body_data,
            session=db.session   
        )

        # Add new airport data to session
        db.session.add(new_airport)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(airport_schema.dump(new_airport)), 201
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"message": "Invalid format given or no data provided."}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Airport name must be unique"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@airport_bp.route("/<int:airport_id>", methods=["PUT", "PATCH"])
def update_airport(airport_id):
    try:
        # Define GET Statement
        stmt = db.select(Airport).where(Airport.id == airport_id)

        # Execute statement
        airport = db.session.scalar(stmt)

        if not airport:
            return {"message": f"Airport with id {airport_id} does not exist/cannot be found."}, 404
        
        body_data = request.get_json()

        updated_airport = airport_schema.load(
            body_data,
            instance=airport,
            partial=True,
            session=db.session
        )

        db.session.commit()
        # Return data
        return jsonify(airport_schema.dump(updated_airport))
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
@airport_bp.route("/<int:airport_id>", methods=["DELETE"])
def delete_airport(airport_id):
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