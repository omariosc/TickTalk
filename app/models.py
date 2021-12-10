# Imports required modules
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Creates SQLAlchemy database
db=SQLAlchemy()

# UserRooms association table
class UserRooms(db.Model):
  __tablename__='UserRooms'
  id=db.Column(db.Integer,primary_key=True)
  user=db.Column(db.ForeignKey('Users.id'))
  room=db.Column(db.ForeignKey('Rooms.id'))
  message=db.relationship('Messages')

# Users table
class Users(UserMixin,db.Model):
  __tablename__='Users'
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String(20),unique=True)
  email=db.Column(db.String(50),unique=True)
  password=db.Column(db.String)
  # Relationship to userrooms
  rooms=db.relationship("Rooms",secondary='UserRooms',back_populates="users")

# Rooms table
class Rooms(db.Model):
  __tablename__='Rooms'
  id=db.Column(db.Integer,primary_key=True)
  # Relationship to userrooms
  users=db.relationship("Users",secondary='UserRooms',back_populates="rooms")
  
# Messages table
class Messages(db.Model):
  __tablename__='Messages'
  id=db.Column(db.Integer,primary_key=True)
  # Foreign userroom id key
  userroom_id=db.Column(db.Integer,db.ForeignKey('UserRooms.id'))
  message=db.Column(db.String)
  datetime=db.Column(db.DateTime(timezone=True))

# Logs table
class Logs(db.Model):
  __tablename__='Logs'
  id=db.Column(db.Integer,primary_key=True)
  # Foreign keys for user id, room id and userroom id
  user_id=db.Column(db.Integer,db.ForeignKey('Users.id'))
  room_id=db.Column(db.Integer,db.ForeignKey('Rooms.id'))
  userroom_id=db.Column(db.Integer,db.ForeignKey('UserRooms.id'))
  message=db.Column(db.String)
  datetime=db.Column(db.DateTime(timezone=True))
  severity=db.Column(db.String)
