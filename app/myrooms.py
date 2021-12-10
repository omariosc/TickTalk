# Imports rquired modules
from flask import Blueprint,render_template
from flask_login import login_required,current_user
from app.models import Rooms,UserRooms,Messages

# Creates myrooms blueprint
myrooms=Blueprint('myrooms',__name__,template_folder='/templates')

# Login required for viewing myrooms
@myrooms.route('/myrooms',methods=['GET'])
@login_required
def show():
  # Gets all rooms
  rooms=Rooms.query.order_by(Rooms.id).all()
  # Initialises arrays and number of rooms
  no_rooms=0
  members=[]
  messages=[]
  joined=[]
  room_ids=[]
  # Iterates through rooms
  for i in range(0,len(rooms)):
    # If user has joined the room
    if UserRooms.query.filter_by(user=current_user.id,room=rooms[i].id).count()>0:
      # Appends values to arrays
      room_ids.append(Rooms.query.filter_by(id=rooms[i].id).one().id)
      userrooms=UserRooms.query.filter_by(room=rooms[i].id).all()
      members.append(len(userrooms))
      count=0
      # Iterates through userrooms
      for j in range(0,len(userrooms)):
        # Increments number of messages
        count += Messages.query.filter_by(userroom_id=userrooms[j].id).count()
      messages.append(count)
      joined.append(1)
      no_rooms += 1
  # Returns final template
  return render_template('roomcard.html',rooms=rooms,no_rooms=no_rooms,room_ids=room_ids,members=members,messages=messages,joined=joined)
