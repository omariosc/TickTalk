from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import db, Users, Rooms, UserRooms, Messages

myrooms = Blueprint('myrooms', __name__, template_folder='/templates')

@myrooms.route('/myrooms', methods=['GET'])
@login_required
def show():
  rooms = Rooms.query.order_by(Rooms.id).all()
  no_rooms = 0
  members = []
  messages = []
  joined = []
  room_ids = []
  for i in range(0,len(rooms)):
    if UserRooms.query.filter_by(user=current_user.id, room=rooms[i].id).count() > 0:
      room_ids.append(Rooms.query.filter_by(id=rooms[i].id).one().id)
      userrooms = UserRooms.query.filter_by(room=rooms[i].id).all()
      members.append(len(userrooms))
      count = 0
      for j in range(0,len(userrooms)):
        count += Messages.query.filter_by(userroom_id=userrooms[j].id).count()
      messages.append(count)
      joined.append(1)
      no_rooms += 1
  return render_template('roomcard.html', rooms=rooms, no_rooms=no_rooms, room_ids=room_ids, members=members, messages=messages, joined=joined)
