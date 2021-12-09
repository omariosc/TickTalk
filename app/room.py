from flask import Blueprint, url_for, redirect
from flask.templating import render_template
from flask_login import login_required, current_user
from app.models import db, Users, Rooms, UserRooms, Messages
from app.logs import log_create_room, log_join_room, log_leave_room

room = Blueprint('room', __name__, template_folder='/templates')

@room.route('/room/<room_id>', methods=['GET'])
@login_required
def show(room_id):
  if len(Rooms.query.filter_by(id=room_id).all()) == 0:
    return redirect(url_for('home.show') + '?error=room-not-exists')
  if UserRooms.query.filter_by(user=current_user.id, room=room_id).count() == 0:
    return redirect(url_for('home.show') + '?error=must-join-room')
  else:
    userrooms = UserRooms.query.filter_by(room=room_id).all()
    messages = []
    for i in range(len(userrooms)):
      userroom_messages = Messages.query.filter_by(userroom_id=userrooms[i].id).all()
      for message in userroom_messages:
        messages.append(message)
    return render_template('chatroom.html', messages=messages, userroom_id=UserRooms.query.filter_by(user=current_user.id, room=room_id).one().id)

@room.route('/room/join/<room_id>', methods=['GET'])
@login_required
def join(room_id):
  if UserRooms.query.filter_by(user=current_user.id, room=room_id).count() > 0:
    return redirect(url_for('home.show') + '?error=already-joined-room')
  else:
    userroom = UserRooms(user=current_user.id, room=room_id)
    db.session.add(userroom)
    db.session.commit()
    log_join_room(userroom)
    return redirect(url_for('home.show') + '?success=joined-room')

@room.route('/room/leave/<room_id>', methods=['GET'])
@login_required
def leave(room_id):
  if UserRooms.query.filter_by(user=current_user.id, room=room_id).count() == 0:
    return redirect(url_for('home.show') + '?error=not-in-room')
  else:
    userroom = UserRooms.query.filter_by(user=current_user.id, room=room_id).one()
    log_leave_room(userroom)
    db.session.delete(userroom)
    db.session.commit()
    return redirect(url_for('home.show') + '?success=left-room')

@room.route('/room/create', methods=['GET'])
@login_required
def create():
  room = Rooms()
  db.session.add(room)
  db.session.commit()
  log_create_room(current_user, room)
  return redirect(url_for('home.show') + '?success=created-room')
