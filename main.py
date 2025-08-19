# Built-in Imports
import os

# Installed imports
from flask import Flask
from dotenv import load_dotenv
from controllers.cli_controller import db_commands

# Created Module Imports
from init import db

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

    # App is returned
    return app