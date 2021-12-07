from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate 
from app.models import db, Users
from app.index import index
from app.login import login
from app.logout import logout
from app.register import register
from app.home import home
from app.settings import settings

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

@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))
