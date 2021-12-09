from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, current 
from app.models import db, Users
from app.index import index
from app.login import login
from app.logout import logout
from app.register import register
from app.home import home
from app.settings import settings
from app.room import room
from app.myrooms import myrooms
from app.logs import log_error

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()
app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(settings)
app.register_blueprint(room)
app.register_blueprint(myrooms)

@login_manager.user_loader
def load_user(id):
  return Users.query.get(int(id))

@app.errorhandler(404)
def error(error):
  if current_user.is_authenticated:
    log_error(user=current_user, error="404")
  else:
    log_error(error="404-not-found", ip=request.remote_addr)
  return render_template('error.html',title='404', message="The page you are looking for was not found."), 404

@app.errorhandler(401)
def error(error):
  if current_user.is_authenticated:
    log_error(user=current_user, error="401")
  else:
    log_error(error="401-unauthorized", ip=request.remote_addr)
  return render_template('error.html',title='401', message="You are not authorized to access the URL requested"), 401
