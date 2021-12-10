from flask import Blueprint,url_for,redirect,request
from flask.templating import render_template
from flask_login import login_required,current_user
from app.models import db,Users,Rooms,UserRooms,Messages
from app.logs import log_create_room,log_delete_messages,log_join_room,log_leave_room,log_error,log_send_message
from datetime import datetime

room=Blueprint('room',__name__,template_folder='/templates')

@room.route('/room/<room_id>',methods=['GET'])
@login_required
def show(room_id):
  if len(Rooms.query.filter_by(id=room_id).all())==0:
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="room-not-exists")
    return redirect(url_for('home.show') + '?error=room-not-exists')
  if UserRooms.query.filter_by(user=current_user.id,room=room_id).count()==0:
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="room-must-join-room")
    return redirect(url_for('home.show') + '?error=must-join-room')
  else:
    userrooms=UserRooms.query.filter_by(room=room_id).all()
    messages=[]
    usernames=[]
    for i in range(len(userrooms)):
      userroom_messages=Messages.query.filter_by(userroom_id=userrooms[i].id).all()
      for message in userroom_messages:
        messages.append(message)
    messages.sort(key=lambda r: r.datetime)
    for message in messages:
      message.datetime = message.datetime.replace(microsecond=0) 
      userid=UserRooms.query.filter_by(id=message.userroom_id).one().user
      username=Users.query.filter_by(id=userid).one().username
      usernames.append(username)
    return render_template('chatroom.html',room_id=room_id,messages=messages,no_messages=len(messages),usernames=usernames,userroom_id=UserRooms.query.filter_by(user=current_user.id,room=room_id).one().id)

@room.route('/room/chat/<room_id>',methods=['GET','POST'])
def chat(room_id):
  if request.method=='POST':
    message=request.form['message']
    userroom=UserRooms.query.filter_by(user=current_user.id,room=room_id).one()
    message_db=Messages(userroom_id=userroom.id,message=message,datetime=datetime.now())
    log_send_message(userroom, message)
    db.session.add(message_db)
    db.session.commit()
    return redirect('/room/'+str(room_id))
  else:
    return redirect('/room/'+str(room_id))

@room.route('/room/join/<room_id>',methods=['GET'])
@login_required
def join(room_id):
  if UserRooms.query.filter_by(user=current_user.id,room=room_id).count()>0:
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="already-joined-room")
    return redirect(url_for('home.show') + '?error=already-joined-room')
  else:
    if len(Rooms.query.filter_by(id=room_id).all())>0:
      userroom=UserRooms(user=current_user.id,room=room_id)
      db.session.add(userroom)
      db.session.commit()
      log_join_room(userroom)
      return redirect(url_for('home.show') + '?success=joined-room')
    else:
      log_error(user=current_user,room=room_id,ip=request.remote_addr,error="room-not-exists")
      return redirect(url_for('home.show') + '?error=room-not-exists')

@room.route('/room/leave/<room_id>',methods=['GET'])
@login_required
def leave(room_id):
  if UserRooms.query.filter_by(user=current_user.id,room=room_id).count()==0:
    log_error(user=current_user,room=room_id,ip=request.remote_addr,error="not-in-room")
    return redirect(url_for('home.show') + '?error=not-in-room')
  else:
    userroom=UserRooms.query.filter_by(user=current_user.id,room=room_id).one()
    messages=Messages.query.filter_by(userroom_id=userroom.id).all()
    for message in messages:
      log_delete_messages(userroom, message)
      db.session.delete(message)
    log_leave_room(userroom)
    db.session.delete(userroom)
    db.session.commit()
    return redirect(url_for('home.show') + '?success=left-room')

@room.route('/room/create',methods=['GET'])
@login_required
def create():
  room=Rooms()
  db.session.add(room)
  db.session.commit()
  log_create_room(current_user,room)
  return redirect(url_for('home.show') + '?success=created-room')
