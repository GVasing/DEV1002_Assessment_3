# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.plane import Plane
from schemas.schemas import plane_schema, planes_schema

# Define Blueprint for plane
plane_bp = Blueprint("plane", __name__, url_prefix="/planes")

# Routes
# GET
@plane_bp.route("/")
def get_planes():
    # Define GET statement
    stmt = db.select(Plane)
    # Execute it
    planes_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = planes_schema.dump(planes_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No plane records found"}, 404
    
# GET /id
@plane_bp.route("/<int:plane_id>")
def get_a_plane(plane_id):
    # Define GET statment
    stmt = db.select(Plane).where(Plane.id == plane_id)

    # Execute it
    plane = db.session.scalar(stmt)

    # Error Handling
    if plane:
        # Serialise
        data = plane_schema.dump(plane)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Plane with id {plane_id} not found."}, 404
    
# POST /
@plane_bp.route("/", methods=["POST"])
def create_a_plane():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Plane Object from Plane class/model with body response data
        # new_plane = Plane(
        #     manufacturer=body_data.get("manufacturer"),
        #     model=body_data.get("model"),
        #     range=body_data.get("range"),
        #     passenger_capacity=body_data.get("passenger_capacity"),
        #     fuel_capacity=body_data.get("fuel_capacity")
        # )
        new_plane = plane_schema.load(
            body_data,
            session=db.session
        )
        # Add new plane data to session
        db.session.add(new_plane)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(plane_schema.dump(new_plane)), 201
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"message": "Invalid format given or no data provided."}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Model name must be unique"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@plane_bp.route("/<int:plane_id>", methods=["PUT", "PATCH"])
def update_plane(plane_id):
    try:
        # Define GET Statement
        stmt = db.select(Plane).where(Plane.id == plane_id)

        # Execute statement
        plane = db.session.scalar(stmt)

        if not plane:
            return {"message": f"Plane with id {plane_id} does not exist/cannot be found."}, 404

        # # If/Elif/Else Conditions
        # if plane:
        #     # Retrieve 'plane' data
        #     body_data = request.get_json()
        #     # Specify changes
        #     plane.manufacturer = body_data.get("manufacturer") or plane.manufacturer
        #     plane.model = body_data.get("model") or plane.model
        #     plane.range = body_data.get("range") or plane.range
        #     plane.passenger_capacity = body_data.get("passenger_capacity") or plane.passenger_capacity
        #     plane.fuel_capacity = body_data.get("fuel_capacity") or plane.fuel_capacity

        body_data = request.get_json()

        updated_plane = plane_schema.load(
            body_data,
            instance=plane,
            partial=True,
            session=db.session
        )
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(plane_schema.dump(updated_plane))
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
@plane_bp.route("/<int:plane_id>", methods=["DELETE"])
def delete_a_plane(plane_id):
        # Find the plane with the plane_id
    stmt = db.select(Plane).where(Plane.id == plane_id)
    plane = db.session.scalar(stmt)
    # if exists
    if plane:
        # delete the plane entry
        db.session.delete(plane)
        db.session.commit()

        return {"message": f"Plane '{plane.manufacturer}: {plane.model}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Plane with id '{plane_id}' does not exist"}, 404