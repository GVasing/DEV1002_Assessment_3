# Built-in Imports
import os

# Installed imports
from flask import Flask
from dotenv import load_dotenv

# Created Module Imports
from init import db
from controllers.cli_controller import db_commands
from controllers.location_controller import location_bp
from controllers.airline_controller import airline_bp
from controllers.plane_controller import plane_bp
from controllers.staff_controller import staff_bp
from controllers.passenger_controller import passenger_bp
from controllers.flight_controller import flight_bp
from controllers.airport_controller import airport_bp
from controllers.booking_controller import booking_bp
from utils.error_handlers import register_error_handlers

# Explain what this does
load_dotenv()

# Explain the purpose of this function
def create_app():

    # Explain the purpose of this variable
    app = Flask(__name__)

    # Explain the purpose of this statement
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Initialise SQL Database
    db.init_app(app)

    # Specify auto sort of keys/attributes to be disabled when GET is requested
    app.json.sort_keys = False

    # Register Blueprint
    app.register_blueprint(db_commands)
    app.register_blueprint(location_bp)
    app.register_blueprint(airline_bp)
    app.register_blueprint(plane_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(passenger_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(airport_bp)
    app.register_blueprint(booking_bp)
    register_error_handlers(app)

    # App is returned
    return app