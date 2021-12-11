from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user
from app.models import db,Users,Rooms,UserRooms,Messages,Logs
from app.index import index
from app.login import login
from app.logout import logout
from app.register import register
from app.home import home
from app.settings import settings
from app.room import room
from app.myrooms import myrooms
from app.logs import log_error
import unittest

class TestCase(unittest.TestCase):
  def setUp(self):
    self.app = Flask(__name__, template_folder='app/templates')
    self.app.config['TESTING'] = True
    self.app.config['WTF_CSRF_ENABLED'] = False
    self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager=LoginManager()
    login_manager.init_app(self.app)
    db.init_app(self.app)
    self.app.app_context().push()
    self.app.register_blueprint(index)
    self.app.register_blueprint(login)
    self.app.register_blueprint(logout)
    self.app.register_blueprint(register)
    self.app.register_blueprint(home)
    self.app.register_blueprint(settings)
    self.app.register_blueprint(room)
    self.app.register_blueprint(myrooms)
    self.app = self.app.test_client()
    @login_manager.user_loader
    def load_user(id):
      return Users.query.get(int(id))
    pass

  def tearDown(self):
    self.app = Flask(__name__, template_folder='app/templates')
    self.app.config['TESTING'] = True
    self.app.config['WTF_CSRF_ENABLED'] = False
    self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager=LoginManager()
    login_manager.init_app(self.app)
    db.init_app(self.app)
    self.app.app_context().push()
    self.app.register_blueprint(index)
    self.app.register_blueprint(login)
    self.app.register_blueprint(logout)
    self.app.register_blueprint(register)
    self.app.register_blueprint(home)
    self.app.register_blueprint(settings)
    self.app.register_blueprint(room)
    self.app.register_blueprint(myrooms)
    self.app = self.app.test_client()
    @login_manager.user_loader
    def load_user(id):
      return Users.query.get(int(id))
    db.session.remove()
    db.drop_all()
    
  def test_load_login(self):
    response = self.app.get('/login',follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
  def test_load_register(self):
    response = self.app.get('/register',follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
  def test_load_index(self):
    response = self.app.get('/',follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
  def test_unauthorized_home(self):
    response = self.app.get('/home',follow_redirects=True)
    self.assertEqual(response.status_code, 401)
    
  def test_unauthorized_settings(self):
    response = self.app.get('/settings',follow_redirects=True)
    self.assertEqual(response.status_code, 401)
    
  def test_unauthorized_create_room(self):
    response = self.app.get('/room/create',follow_redirects=True)
    self.assertEqual(response.status_code, 401)
    
  def test_unauthorized_join_room(self):
    response = self.app.get('/room/join/1',follow_redirects=True)
    self.assertEqual(response.status_code, 401)
    
  def test_unauthorized_leave_room(self):
    response = self.app.get('/room/leave/1',follow_redirects=True)
    self.assertEqual(response.status_code, 401)
    
  def test_unauthorized_view_room(self):
    response = self.app.get('/room/1',follow_redirects=True)
    self.assertEqual(response.status_code, 401)
    
  def test_not_found(self):
    response = self.app.get('/randomurl',follow_redirects=True)
    self.assertEqual(response.status_code, 404)
  

if __name__ == '__main__':
  unittest.main()