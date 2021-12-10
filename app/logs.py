# Imports required module
from app.models import db,Logs,Users,Rooms
from datetime import datetime

# Logs user logout
def log_logout(user):
  db.session.add(Logs(
    user_id=user.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+user.username+"\" logged out"))
  db.session.commit()

# Logs user login
def log_user_login(user):
  db.session.add(Logs(
    user_id=user.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+user.username+"\" logged in"))
  db.session.commit()

# Logs user creation
def log_create_user(user):
  db.session.add(Logs(
    user_id=user.id,
    datetime=datetime.now(),
    severity="INFO",
    message="created user \""+user.username+"\""))
  db.session.commit()
  log_user_login(user)

# Logs user changed password
def log_change_password(user):
  db.session.add(Logs(
    user_id=user.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+user.username+"\" changed password"))
  db.session.commit()

# Logs room creation by user
def log_create_room(user,room):
  db.session.add(Logs(
    user_id=user.id,
    room_id=room.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+user.username+"\" created room "+str(room.id)))
  db.session.commit()

# Logs user joining room
def log_join_room(userroom):
  username=str(Users.query.filter_by(id=userroom.user).one().username)
  room=str(Rooms.query.filter_by(id=userroom.room).one().id)
  db.session.add(Logs(
    user_id=userroom.user,
    room_id=userroom.room,
    userroom_id=userroom.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+username+"\" joined room "+room))
  db.session.commit()

# Logs message deletion
def log_delete_messages(userroom, message):
  username=str(Users.query.filter_by(id=userroom.user).one().username)
  room=str(Rooms.query.filter_by(id=userroom.room).one().id)
  db.session.add(Logs(
    user_id=userroom.user,
    room_id=userroom.room,
    userroom_id=userroom.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+username+"\" deleted message \""+message.message+"\" in room"+room))
  db.session.commit()

# Logs leaving room
def log_leave_room(userroom):
  username=str(Users.query.filter_by(id=userroom.user).one().username)
  room=str(Rooms.query.filter_by(id=userroom.room).one().id)
  db.session.add(Logs(
    user_id=userroom.user,
    room_id=userroom.room,
    userroom_id=userroom.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+username+"\" left room "+room))
  db.session.commit()

# Logs sending message
def log_send_message(userroom,message):
  username=str(Users.query.filter_by(id=userroom.user).one().username)
  room=str(Rooms.query.filter_by(id=userroom.room).one().id)
  db.session.add(Logs(
    user_id=userroom.user,
    room_id=userroom.room,
    userroom_id=userroom.id,
    datetime=datetime.now(),
    severity="INFO",
    message="user \""+username+"\" sent message \""+message+"\" room "+room))
  db.session.commit()

# Logs error
def log_error(user=0,room=0,userroom=0,error="",ip=0):
  error_log=Logs(datetime=datetime.now(),severity="WARNING")
  message=""
  # Concatenates message to error
  if ip != 0:
    message += "ip: \""+str(ip)+"\"; "
  if len(error)>0:
    message += "error: \""+error+"\"; "
  if user != 0:
    message += "user id: \""+str(user.id)+"\"; "
    error_log.user_id=user.id
  if room != 0:
    message += "room id: \""+str(room)+"\"; "
    error_log.room_id=room
  if userroom != 0:
    message += "userroom id: \""+str(userroom.id)+"\"; "
    error_log.userroom_id=userroom.id
  error_log.message=message
  # Adds error to database
  db.session.add(error_log)
  db.session.commit()