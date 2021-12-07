from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String)
  
class Room(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  count = db.Column(db.Integer)

class Messages(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  room = db.Column(db.Integer)
  user = db.Column(db.Integer)
  message = db.Column(db.String)
