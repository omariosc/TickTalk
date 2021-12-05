# Imports required modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

# Creates Flask app
app = Flask(__name__)
# Configures app using configuration file
app.config.from_object('config')
# Creates SQLAlchemy database for the app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Imports views and models
from app import views, models
