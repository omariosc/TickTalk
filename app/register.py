import sqlalchemy
from flask import Blueprint, url_for, render_template, redirect, request
from flask.helpers import make_response
from flask_login import LoginManager
from flask_login import login_user
from werkzeug.security import generate_password_hash
from app.models import db, Users
from app.logs import log_create_user

register = Blueprint('register', __name__, template_folder='/templates')
login_manager = LoginManager()
login_manager.init_app(register)
regtxt = "register.show"

@register.route('/register', methods=['GET', 'POST'])
def show():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']
    if username and email and password and confirm_password:
      if password == confirm_password:
        hashed_password = generate_password_hash(password, method='sha256')
        try:
          new_user = Users(username=username, email=email,password=hashed_password)
          db.session.add(new_user)
          db.session.commit()
        except sqlalchemy.exc.IntegrityError:
          return redirect(url_for(regtxt) + '?error=user-or-email-exists')
        login_user(new_user)
        log_create_user(new_user)
        return redirect(url_for('home.show') + '?success=account-created')
      else:
        return redirect(url_for(regtxt) + '?error=password-dont-match')
    else:
      return redirect(url_for(regtxt) + '?error=missing-fields')
  else:
    return render_template('register.html', title="Register")
