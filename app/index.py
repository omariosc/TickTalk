# Imports reuired modules
from flask import Blueprint,redirect
from flask_login import current_user

# Index blueprint
index=Blueprint('index',__name__,template_folder='/templates')

# Route for index
@index.route('/',methods=['GET'])
def show():
  # If user is logged in
  if current_user.is_authenticated:
    # Redirect to home page
    return redirect('home')
  # Otherwise...
  else: 
    # Redirect to login page
    return redirect('login')