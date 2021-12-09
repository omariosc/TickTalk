from flask import Blueprint, url_for, redirect
from flask.templating import render_template
from flask_login import login_required, current_user
from app.models import db, Rooms, UserRooms

room = Blueprint('room', __name__, template_folder='/templates')

@room.route('/room/<room_id>', methods=['GET'])
@login_required
def show(room_id):
  return render_template('chatroom.html')

@room.route('/room/join/<room_id>', methods=['GET'])
@login_required
def join(room_id):
  if UserRooms.query.filter_by(user=current_user.id, room=room_id).count() > 0:
    return redirect(url_for('home.show') + '?error=already-joined-room')
  else:
    userroom = UserRooms(user=current_user.id, room=room_id)
    db.session.add(userroom)
    db.session.commit()
  return redirect(url_for('home.show') + '?success=joined-room')

@room.route('/room/leave/<room_id>', methods=['GET'])
@login_required
def leave(room_id):
  if UserRooms.query.filter_by(user=current_user.id, room=room_id).count() == 0:
    return redirect(url_for('home.show') + '?error=not-in-room')
  else:
    db.session.delete(UserRooms.query.filter_by(user=current_user.id, room=room_id).one())
    db.session.commit()
  return redirect(url_for('home.show') + '?success=left-room')

@room.route('/room/create', methods=['GET'])
@login_required
def create():
  room = Rooms()
  db.session.add(room)
  db.session.commit()
  return redirect(url_for('home.show') + '?success=created-room')
