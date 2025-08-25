# Installed imports
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes

# Created Module Imports
from init import db
from models.booking import Booking
from schemas.schemas import booking_schema, bookings_schema

# Define Blueprint for booking
booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")

# Routes
# GET
@booking_bp.route("/")
def get_bookings():
    # Define GET statement
    stmt = db.select(Booking)
    # Execute it
    bookings_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = bookings_schema.dump(bookings_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "No booking records found"}, 404
    
# GET /id
@booking_bp.route("/<int:booking_id>")
def get_a_booking(booking_id):
    # Define GET statment
    stmt = db.select(Booking).where(Booking.id == booking_id)

    # Execute it
    booking = db.session.scalar(stmt)

    # Error Handling
    if booking:
        # Serialise
        data = booking_schema.dump(booking)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Booking with id {booking_id} not found."}, 404
    
# POST /
@booking_bp.route("/", methods=["POST"])
def create_booking():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Booking Object from Booking class/model with body response data
        # new_booking = Booking(
        #     cabin_class=body_data.get("cabin_class"),
        #     checked_baggage=body_data.get("checked_baggage"),
        #     seat_selected=body_data.get("seat_selected"),
        #     meal_ordered=body_data.get("meal_ordered"),
        #     ticket_price=body_data.get("ticket_price"),
        #     airport_id=body_data.get("airport_id"),
        #     flight_id=body_data.get("flight_id"),
        #     passenger_id=body_data.get("passenger_id")
        # )

        new_booking = booking_schema.load(
            body_data,
            session=db.session
        )

        # Add new booking data to session
        db.session.add(new_booking)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(booking_schema.dump(new_booking)), 201
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
@booking_bp.route("/<int:booking_id>", methods=["PUT", "PATCH"])
def update_booking(booking_id):
    try:
        # Define GET Statement
        stmt = db.select(Booking).where(Booking.id == booking_id)

        # Execute statement
        booking = db.session.scalar(stmt)

        if not booking:
            return {"message": f"Booking with id {booking_id} does not exist/cannot be found."}, 404

        # If/Elif/Else Conditions
        # if booking:
        #     # Retrieve 'booking' data
        #     body_data = request.get_json()
        #     # Specify changes
        #     booking.cabin_class = body_data.get("cabin_class") or booking.cabin_class
        #     booking.checked_baggage = body_data.get("checked_baggage") or booking.checked_baggage
        #     booking.baggage_amount = body_data.get("baggage_amount") or booking.baggage_amount
        #     booking.seat_selected = body_data.get("seat_selected") or booking.seat_selected
        #     booking.meal_ordered = body_data.get("meal_ordered") or booking.meal_ordered
        #     booking.ticket_price = body_data.get("ticket_price") or booking.ticket_price
        #     booking.airport_id = body_data.get("airport_id") or booking.airport_id
        #     booking.flight_id = body_data.get("flight_id") or booking.flight_id
        #     booking.passenger_id = body_data.get("passenger_id") or booking.passenger_id

        body_data = request.get_json()

        updated_booking = booking_schema.load(
            body_data,
            instance=booking,
            partial=True,
            session=db.session
        )
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(booking_schema.dump(updated_booking))
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
@booking_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
        # Find the booking with the booking_id
    stmt = db.select(Booking).where(Booking.id == booking_id)
    booking = db.session.scalar(stmt)
    # if exists
    if booking:
        # delete the booking entry
        db.session.delete(booking)
        db.session.commit()

        return {"message": f"Booking '{booking_id}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Booking with id '{booking_id}' does not exist"}, 404