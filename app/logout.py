# Imports required modules
from flask import Blueprint,url_for,redirect,request,flash
from flask_login import LoginManager,login_required,logout_user,current_user
from app.logs import log_logout,log_error

# Logout blueprint
logout=Blueprint('logout',__name__,template_folder='/templates')
login_manager=LoginManager()
login_manager.init_app(logout)

# Login required to logout
@logout.route('/logout')
@login_required
def show():
  # If user is logged in
  if current_user.is_authenticated:
    flash("Logged out")
    # Logout user and log the logout
    log_logout(current_user)
    logout_user()
    return redirect(url_for('login.show') + '?success=logged-out')
  # Otherwise...
  else:
    flash("You are not logged in", "error")
    # Log error
    log_error(ip=request.remote_addr,error="logout-not-logged-in")
    return redirect(url_for('login.show') + '?error=not-logged-in')