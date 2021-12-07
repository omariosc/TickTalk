from flask import Blueprint, redirect
from flask_login import current_user

index = Blueprint('index', __name__, template_folder='/templates')

@index.route('/', methods=['GET'])
def show():
  if current_user.is_authenticated:
    return redirect('home') 
  return redirect('login')