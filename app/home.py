from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user
from app.models import db, Users, Rooms, UserRooms, Messages

home = Blueprint('home', __name__, template_folder='/templates')
login_manager = LoginManager()
login_manager.init_app(home)

@home.route('/home', methods=['GET'])
@login_required
def show():
  rooms = Rooms.query.order_by(Rooms.id).all()
  members = []
  messages = []
  joined = []
  for i in range(0,len(rooms)):
    userrooms = UserRooms.query.filter_by(room=rooms[i].id).all()
    members.append(len(userrooms))
    count = 0
    for j in range(0,len(userrooms)):
      count += Messages.query.filter_by(userroom_id=userrooms[j].id).count()
    messages.append(count)
    if UserRooms.query.filter_by(user=current_user.id, room=rooms[i].id).count() > 0:
      joined.append(1)
    else:
      joined.append(0)
  return render_template('roomcard.html', rooms=rooms, no_rooms=len(rooms), members=members, messages=messages, joined=joined)
