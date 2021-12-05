# Imports required modules
from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

# Creates the database
db.create_all()