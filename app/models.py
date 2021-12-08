from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class UserRooms(db.Model):
  __tablename__ = 'UserRooms'
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.ForeignKey('Users.id'))
  room = db.Column(db.ForeignKey('Rooms.id'))
  message = db.relationship("UserRoom", secondary='Messages')

class Users(UserMixin, db.Model):
  __tablename__ = 'Users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String)
  room = db.relationship("User", secondary='UserRooms')

class Rooms(db.Model):
  __tablename__ = 'Rooms'
  id = db.Column(db.Integer, primary_key=True)
  user = db.relationship("Room", secondary='UserRooms')
  
class Messages(db.Model):
  __tablename__ = 'Messages'
  id = db.Column(db.Integer, primary_key=True)
  userroom = db.Column(db.ForeignKey('UserRooms.id'))
  message = db.Column(db.String)
  time = db.Column(db.Date)
