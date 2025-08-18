# Built-in Imports
import os

# Installed imports
from flask import Flask
from dotenv import load_dotenv

# Created Module Imports
from init import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Initialise SQL Database
    db.init_app(app)

    return app