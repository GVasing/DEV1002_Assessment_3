# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.staff import Staff
from schemas.schemas import staff_schema, staffs_schema

# Define Blueprint for staff
staff_bp = Blueprint("staff", __name__, url_prefix="/staff")

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
def get_a_staff(staff_id):
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
def create_a_staff():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Staff Object from Staff class/model with body response data
        new_staff = Staff(
            name=body_data.get("name"),
            age=body_data.get("age"),
            gender=body_data.get("gender"),
            employment=body_data.get("employment"),
            position=body_data.get("position"),
            salary=body_data.get("salary"),
            years_worked=body_data.get("years_worked"),
        )
        # Add new staff data to session
        db.session.add(new_staff)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(staff_schema.dump(new_staff)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        else:
            return {"message": "Unexpected Error Occured"}, 400
        
# PUT/PATCH /id
@staff_bp.route("/<int:staff_id>", methods=["PUT", "PATCH"])
def update_staff(staff_id):
    # Define GET Statement
    stmt = db.select(Staff).where(Staff.id == staff_id)

    # Execute statement
    staff = db.session.scalar(stmt)

    # If/Elif/Else Conditions
    if staff:
        # Retrieve 'staff' data
        body_data = request.get_json()
        # Specify changes
        staff.name = body_data.get("name") or staff.name
        staff.age = body_data.get("age") or staff.age
        staff.gender = body_data.get("gender") or staff.gender
        staff.employment = body_data.get("employment") or staff.employment
        staff.position = body_data.get("position") or staff.position
        staff.salary = body_data.get("salary") or staff.salary
        staff.years_worked = body_data.get("years_worked") or staff.years_worked
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(staff_schema.dump(staff))
    else:
        return {"message": f"Staff with id {staff_id} does not exist/cannot be found."}, 404

# DELETE /id
@staff_bp.route("/<int:staff_id>", methods=["DELETE"])
def delete_a_staff(staff_id):
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