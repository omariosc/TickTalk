# Imports required modules
from flask import Blueprint,url_for,render_template,redirect,request,flash
from flask_login import LoginManager,login_user,current_user
from werkzeug.security import check_password_hash
from app.models import db,Users
from app.logs import log_user_login,log_error

# Login blueprint
login=Blueprint('login',__name__,template_folder='/templates')
login_manager=LoginManager()
login_manager.init_app(login)

# Login route
@login.route('/login',methods=['GET','POST'])
def show():
  # If user is logged in, redirect to home page
  if current_user.is_authenticated:
    return redirect('home')
  # If user submits form
  if request.method=='POST':
    # Get username and password inputs
    username=request.form['username']
    password=request.form['password']
    # Gets the user record for the username
    user=Users.query.filter_by(username=username).first()
    # If the user exists
    if user:
      # If hashed paswords match
      if check_password_hash(user.password,password):
        # Logs user in
        login_user(user)
        # Logs user login
        log_user_login(user)
        flash("Logged in")
        return redirect(url_for('home.show')+ '?success=logged-in')
      # If incorrect password
      else:
        flash("Incorrect password", "error")
        # Logs error
        log_error(user=user,ip=request.remote_addr,error="login-incorrect-password")
        return redirect(url_for('login.show') + '?error=incorrect-password')
    # If user does not exist
    else:
      flash("User "+str(username)+" does not exist", "error")
      # Logs error
      log_error(ip=request.remote_addr,error="login-user-not-found")
      return redirect(url_for('login.show') + '?error=user-not-found')
  # Otherwise...
  else:
    # Returns login template
    return render_template('login.html',title="Login")
