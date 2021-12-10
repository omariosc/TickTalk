# Import required modules
from flask import Blueprint,url_for,render_template,redirect,request,flash
from flask_login import LoginManager,current_user
from flask_login import login_user
from werkzeug.security import generate_password_hash
from app.models import db,Users
from app.logs import log_create_user,log_error

# Creates register blueprint
register=Blueprint('register',__name__,template_folder='/templates')
login_manager=LoginManager()
login_manager.init_app(register)

# For url redirect
regtxt="register.show"

# Register route
@register.route('/register',methods=['GET','POST'])
def show():
  # If user is already logged in
  if current_user.is_authenticated:
    # Redirects user to home page
    return redirect('home')
  # If user submits details
  if request.method=='POST':
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    confirm_password=request.form['confirm-password']
    # Checks is values exist
    if username and email and password and confirm_password:
      # Checks if username exists
      if (Users.query.filter_by(username=username).count()==0):
        # Checks if email exists
        if (Users.query.filter_by(email=email).count()==0):
          # If the passwords match
          if password==confirm_password:
            # Hashes password
            hashed_password=generate_password_hash(password,method='sha256')
            # Attempts to create the new user
            new_user=Users(username=username,email=email,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            # Logs user in and logs user creation
            login_user(new_user)
            log_create_user(new_user)
            flash("Account created")
            return redirect(url_for('home.show') + '?success=account-created')
          # If passwords dont match
          else:
            flash("Passwords don't match", "error")
            # Logs error
            log_error(ip=request.remote_addr,error="register-passwords-dont-match")
            return redirect(url_for(regtxt) + '?error=passwords-dont-match')
        # If email already exists
        else:
          flash("Email already exists", "error")
          # Logs error
          log_error(ip=request.remote_addr,error="register-email-already-exists")
          return redirect('/register' + '?error=email-already-exists')
      # If user already exists
      else:
        flash("Username already exists", "error")
        # Logs error
        log_error(ip=request.remote_addr,error="register-username-already-exists")
        return redirect('/register' + '?error=username-already-exists')
    # If there are missing fields
    else:
      flash("Missing fields", "error")
      # Logs error
      log_error(ip=request.remote_addr,error="register-missing-fields")
      return redirect(url_for(regtxt) + '?error=missing-fields')
  # Otherwise...
  else:
    # Returns template
    return render_template('register.html',title="Register")
