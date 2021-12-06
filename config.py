# Enables CSRF and sets secret key
WTF_CSRF_ENABLED = True
SECRET_KEY = 'sc20osc'

# Sets path and configuration for database
SQLALCHEMY_DATABASE_URI = 'sqlite:///../users.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True