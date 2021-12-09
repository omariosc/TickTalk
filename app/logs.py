from app.models import db, Logs, Users, Rooms
from datetime import datetime

def log_user_login(user):
  db.session.add(Logs(
    user_id=user.id, 
    datetime=datetime.now(),
    message="user \""+user.username+"\" logged in"))
  db.session.commit()

def log_create_user(user):
  db.session.add(Logs(
    user_id=user.id, 
    datetime=datetime.now(), 
    message="created \""+user.username+"\""))
  db.session.commit()
  log_user_login(user)

def log_change_password(user):
  db.session.add(Logs(
    user_id=user.id, 
    datetime=datetime.now(), 
    message="user \""+user.username+"\" changed password"))
  db.session.commit()

def log_create_room(user, room):
  db.session.add(Logs(
    user_id=user.id,
    room_id=room.id,
    datetime=datetime.now(),
    message="user \""+user.username+"\" created room "+str(room.id)))
  db.session.commit()

def log_join_room(userroom):
  username = str(Users.query.filter_by(id=userroom.user).one().username)
  room = str(Rooms.query.filter_by(id=userroom.room).one().id)
  db.session.add(Logs(
    user_id=userroom.user,
    room_id=userroom.room,
    userroom_id=userroom.id, 
    datetime=datetime.now(), 
    message="user \""+username+"\" joined room "+room))
  db.session.commit()

def log_leave_room(userroom):
  username = str(Users.query.filter_by(id=userroom.user).one().username)
  room = str(Rooms.query.filter_by(id=userroom.room).one().id)
  db.session.add(Logs(
    user_id=userroom.user,
    room_id=userroom.room,
    userroom_id=userroom.id, 
    datetime=datetime.now(), 
    message="user \""+username+"\" left room "+room))
  db.session.commit()

def log_send_message(userroom, message):
  username = str(Users.query.filter_by(id=userroom.user).one().username)
  room = str(Rooms.query.filter_by(id=userroom.room).one().id)
  db.session.add(Logs(
    user_id=userroom.user,
    room_id=userroom.room,
    userroom_id=userroom.id,
    datetime=datetime.now(),
    message="user \""+username+"\" sent message \""+message+"\" room "+room))
  db.session.commit()
