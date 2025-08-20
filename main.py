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

    # Register Blueprint
    app.register_blueprint(db_commands)
    app.register_blueprint(location_bp)
    app.register_blueprint(airline_bp)
    app.register_blueprint(plane_bp)

    # App is returned
    return app