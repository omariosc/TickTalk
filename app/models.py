from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String)

class Rooms(db.Model):
  id = db.Column(db.Integer, primary_key=True)

class UsersRooms(db.Model):
  user_id = db.Column(db.Integer, db.ForeignKey(Users.id), primary_key=True)
  room_id = db.Column(db.Integer, db.ForeignKey(Rooms.id), primary_key=True)  
  user = db.relationship('User', foreign_keys='Users.id')
  room = db.relationship('Room', foreign_keys='Rooms.id')

class Messages(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
  room_id = db.Column(db.Integer, db.ForeignKey(Rooms.id))
  message = db.Column(db.String)
  time = db.Column(db.Date)
  user = db.relationship('User', foreign_keys='Users.id')
  room = db.relationship('Room', foreign_keys='Rooms.id')
