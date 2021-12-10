# Import required modules
from flask import Blueprint,url_for,redirect,request,flash
from flask.templating import render_template
from flask_login import login_required,current_user
from app.models import db,Users,Rooms,UserRooms,Messages
from app.logs import log_create_room,log_delete_messages,log_join_room,log_leave_room,log_error,log_send_message
from datetime import datetime

# Creates room blueprint
room=Blueprint('room',__name__,template_folder='/templates')

# Login required to view a room
@room.route('/room/<room_id>',methods=['GET'])
@login_required
def show(room_id):
  # Check if room exists
  if len(Rooms.query.filter_by(id=room_id).all())==0:
    flash("Room "+str(room_id)+" does not exist", "error")
    # Logs the error
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="room-not-exists")
    return redirect(url_for('home.show') + '?error=room-not-exists')
  # Checks if user is in the room
  if UserRooms.query.filter_by(user=current_user.id,room=room_id).count()==0:
    flash("You are not in Room "+str(room_id), "error")
    # Logs the error
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="room-must-join-room")
    return redirect(url_for('home.show') + '?error=must-join-room')
  # Otherwise...
  else:
    # Gets all userroom ids for the specific room
    userrooms=UserRooms.query.filter_by(room=room_id).all()
    # Initialises empty arrays
    messages=[]
    usernames=[]
    times=[]
    # Iterates through userrooms
    for i in range(len(userrooms)):
      # Gets all messages with the userroom id
      userroom_messages=Messages.query.filter_by(userroom_id=userrooms[i].id).all()
      # Iterates through messages
      for message in userroom_messages:
        # Appends the message to the array
        messages.append(message)
    # Sorts the messages by datetime
    messages.sort(key=lambda r: r.datetime)
    # Iteartes through messages
    for message in messages:
      # Appends formatted time to array
      times.append(message.datetime.strftime("%H:%m %p | %B %d"))
      # Sets the user id and username
      userid=UserRooms.query.filter_by(id=message.userroom_id).one().user
      username=Users.query.filter_by(id=userid).one().username
      # Appends username corresponding to message to array
      usernames.append(username)
    return render_template('chatroom.html',room_id=room_id,messages=messages,no_messages=len(messages),usernames=usernames,userroom_id=UserRooms.query.filter_by(user=current_user.id,room=room_id).one().id,times=times)

# Login required when user sends a message
@room.route('/room/chat/<room_id>',methods=['GET','POST'])
@login_required
def chat(room_id):
  # If user sends a message
  if request.method=='POST':
    # Stores message
    message=request.form['message']
    # Gets userroom and creates message for database
    userroom=UserRooms.query.filter_by(user=current_user.id,room=room_id).one()
    message_db=Messages(userroom_id=userroom.id,message=message,datetime=datetime.now())
    # Logs sending message
    log_send_message(userroom, message)
    # Adds message to database
    db.session.add(message_db)
    db.session.commit()
    return redirect('/room/'+str(room_id))
  # Otherwise...
  else:
    return redirect('/room/'+str(room_id))

# Login required when user joins a room
@room.route('/room/join/<room_id>',methods=['GET'])
@login_required
def join(room_id):
  # Checks if user is already in the room
  if UserRooms.query.filter_by(user=current_user.id,room=room_id).count()>0:
    flash("Already joined Room "+str(room_id), "error")
    # Logs error
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="already-joined-room")
    return redirect(url_for('home.show') + '?error=already-joined-room')
  # Otherwise...
  else:
    # If the room exists...
    if len(Rooms.query.filter_by(id=room_id).all())>0:
      # Creates the userroom, adds to database and creates log
      userroom=UserRooms(user=current_user.id,room=room_id)
      db.session.add(userroom)
      db.session.commit()
      log_join_room(userroom)
      flash("Joined Room "+str(room_id))
      return redirect(url_for('home.show') + '?success=joined-room')
    else:
      flash("Room "+str(room_id)+" does not exist", "error")
      # Logs error
      log_error(user=current_user,room=room_id,ip=request.remote_addr,error="room-not-exists")
      return redirect(url_for('home.show') + '?error=room-not-exists')

# Login required for leaving room
@room.route('/room/leave/<room_id>',methods=['GET'])
@login_required
def leave(room_id):
  # If user is not in room
  if UserRooms.query.filter_by(user=current_user.id,room=room_id).count()==0:
    flash("You are not in Room "+str(room_id), "error")
    # Log error
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="not-in-room")
    return redirect(url_for('home.show') + '?error=not-in-room')
  # Otherwise...
  else:
    # Gets the userroom and all messages from the user in the specific room
    userroom=UserRooms.query.filter_by(user=current_user.id,room=room_id).one()
    messages=Messages.query.filter_by(userroom_id=userroom.id).all()
    # Iterates through messages
    for message in messages:
      # Logs deleting the message
      log_delete_messages(userroom, message)
      # Deletes the message from the database
      db.session.delete(message)
    # Logs leaving the room
    log_leave_room(userroom)
    db.session.delete(userroom)
    db.session.commit()
    flash("Left Room "+str(room_id))
    return redirect(url_for('home.show') + '?success=left-room')

# Login requried for creating room
@room.route('/room/create',methods=['GET'])
@login_required
def create():
  # Creates the room
  room=Rooms()
  db.session.add(room)
  db.session.commit()
  # Logs the room creation by the user
  log_create_room(current_user,room)
  flash("Created Room "+str(room.id))
  return redirect(url_for('home.show') + '?success=created-room')
