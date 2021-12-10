# Improts required modules
from flask import Flask,render_template,request
from flask_login import LoginManager,current_user
from flask_migrate import Migrate
from app.models import db,Users

# Imports blueprints
from app.index import index
from app.login import login
from app.logout import logout
from app.register import register
from app.home import home
from app.settings import settings
from app.room import room
from app.myrooms import myrooms
from app.logs import log_error

# Creates flask app
app=Flask(__name__)

# Configures app from config file
app.config.from_object('config')

# Creates login manager and initialises to app
login_manager=LoginManager()
login_manager.init_app(app)

# Initialises database to app and creates migration
db.init_app(app)
migrate=Migrate(app,db)

# Registers blueprints
app.app_context().push()
app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(settings)
app.register_blueprint(room)
app.register_blueprint(myrooms)

# Loads user id
@login_manager.user_loader
def load_user(id):
  return Users.query.get(int(id))

# Handles 404 errors
@app.errorhandler(404)
def error(error):
  # If user is logged in
  if current_user.is_authenticated:
    # Logs user and 404 error code
    log_error(user=current_user,error="404")
  # Otherwise...
  else:
    # Log 404 error code and ip address
    log_error(error="404-not-found",ip=request.remote_addr)
  # Return error template
  return render_template('error.html',title='404',message="The page you are looking for was not found."),404

# Handles 401 errors
@app.errorhandler(401)
def error(error):
  # If user is logged in
  if current_user.is_authenticated:
    # Logs user and 401 error code
    log_error(user=current_user,error="401")
  # Otherwise...
  else:
    # Log 401 error code and ip address
    log_error(error="401-unauthorized",ip=request.remote_addr)
  # Return error template
  return render_template('error.html',title='401',message="You are not authorized to access the URL requested"),401
