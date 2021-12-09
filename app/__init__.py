from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate 
from app.models import db, Users
from app.index import index
from app.login import login
from app.logout import logout
from app.register import register
from app.home import home
from app.settings import settings
from app.room import room

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

@login_manager.user_loader
def load_user(id):
  return Users.query.get(int(id))

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html',title='404'), 404