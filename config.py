# Imports required os module
import os

# Enables CSRF and sets secret key
WTF_CSRF_ENABLED = True
SECRET_KEY = 'sc20osc'

# Sets path and configuration for database
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
