# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.staff import Staff
from schemas.schemas import staff_schema, staffs_schema

# Define Blueprint for staff
staff_bp = Blueprint("staff", __name__, url_prefix="/staffs")

# Routes
# GET
@staff_bp.route("/")
def get_staff():
    # Define GET statement
    stmt = db.select(Staff)
    # Execute it
    staffs_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = staffs_schema.dump(staffs_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No staff records found"}, 404
    
# GET /id
@staff_bp.route("/<int:staff_id>")
def get_a_staff_member(staff_id):
    # Define GET statment
    stmt = db.select(Staff).where(Staff.id == staff_id)

    # Execute it
    staff = db.session.scalar(stmt)

    # Error Handling
    if staff:
        # Serialise
        data = staff_schema.dump(staff)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Staff with id {staff_id} not found."}, 404
    
# POST /
@staff_bp.route("/", methods=["POST"])
def create_staff():
    try:
        # GET info from the request body
        body_data = request.get_json()

        # errors = staff_schema.validate(body_data, session=db.session)

        # if errors:
        #     return {"message": "Validation failed", "errors": errors}, 400
        
        # # # Create a Staff Object from Staff class/model with body response data
        # new_staff = Staff(
        #     name=body_data.get("name"),
        #     age=body_data.get("age"),
        #     gender=body_data.get("gender"),
        #     employment=body_data.get("employment"),
        #     position=body_data.get("position"),
        #     salary=body_data.get("salary"),
        #     years_worked=body_data.get("years_worked"),
        #     airport_id=body_data.get("airport_id")
        # )

        new_staff = staff_schema.load(
            body_data,
            session=db.session
        )

        # Add new staff data to session
        db.session.add(new_staff)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(staff_schema.dump(new_staff)), 201
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"message": "Invalid format given or no data provided."}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@staff_bp.route("/<int:staff_id>", methods=["PUT", "PATCH"])
def update_staff(staff_id):
    try:
        # Define GET Statement
        stmt = db.select(Staff).where(Staff.id == staff_id)

        # Execute statement
        staff = db.session.scalar(stmt)

        if not staff:
            return {"message": f"Staff with id {staff_id} does not exist/cannot be found."}, 404

        # # If/Elif/Else Conditions
        # if staff:
        #     # Retrieve 'staff' data
        #     body_data = request.get_json()
        #     # Specify changes
        #     staff.name = body_data.get("name") or staff.name
        #     staff.age = body_data.get("age") or staff.age
        #     staff.gender = body_data.get("gender") or staff.gender
        #     staff.employment = body_data.get("employment") or staff.employment
        #     staff.position = body_data.get("position") or staff.position
        #     staff.salary = body_data.get("salary") or staff.salary
        #     staff.years_worked = body_data.get("years_worked") or staff.years_worked
        #     staff.airport_id = body_data.get("airport_id") or staff.airport_id
        # else:
        #     return {"message": f"Staff with id {staff_id} does not exist/cannot be found."}, 404

        body_data = request.get_json()

        updated_staff = staff_schema.load(
            body_data,
            instance=staff,
            partial=True,
            session=db.session
        )

        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(staff_schema.dump(updated_staff))
    # except ValidationError as err:
    #     return err.messages, 400
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
@staff_bp.route("/<int:staff_id>", methods=["DELETE"])
def delete_staff(staff_id):
        # Find the staff with the staff_id
    stmt = db.select(Staff).where(Staff.id == staff_id)
    staff = db.session.scalar(stmt)
    # if exists
    if staff:
        # delete the staff entry
        db.session.delete(staff)
        db.session.commit()

        return {"message": f"Staff member'{staff.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Staff with id '{staff_id}' does not exist"}, 404