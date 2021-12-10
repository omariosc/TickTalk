# Imports required modules
from flask import Blueprint,render_template
from flask_login import LoginManager,login_required,current_user
from app.models import db,Users,Rooms,UserRooms,Messages

# Home blueprint
home=Blueprint('home',__name__,template_folder='/templates')
login_manager=LoginManager()
login_manager.init_app(home)

# Login required for home page
@home.route('/home',methods=['GET'])
@login_required
def show():
  # Gets rooms
  rooms=Rooms.query.order_by(Rooms.id).all()
  # Initialises empty arrays
  members=[]
  messages=[]
  joined=[]
  room_ids=[]
  # Iterates through rooms
  for i in range(0,len(rooms)):
    # Appends values to arrays
    room_ids.append(Rooms.query.filter_by(id=rooms[i].id).one().id)
    userrooms=UserRooms.query.filter_by(room=rooms[i].id).all()
    members.append(len(userrooms))
    count=0
    # Iterates through userrooms
    for j in range(0,len(userrooms)):
      # Increments number of messages
      count += Messages.query.filter_by(userroom_id=userrooms[j].id).count()
    # Appends the number of messages to the arau
    messages.append(count)
    # If user has joined
    if UserRooms.query.filter_by(user=current_user.id,room=rooms[i].id).count()>0:
      # Append 1
      joined.append(1)
    # Otherwise...
    else:
      # Append 0
      joined.append(0)
  # Return final roomcard template
  return render_template('roomcard.html',rooms=rooms,no_rooms=len(rooms),room_ids=room_ids,members=members,messages=messages,joined=joined)
