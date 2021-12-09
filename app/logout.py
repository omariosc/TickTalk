from flask import Blueprint, url_for, redirect, request
from flask_login import LoginManager, login_required, logout_user, current_user
from app.logs import log_logout, log_error

logout = Blueprint('logout', __name__, template_folder='/templates')
login_manager = LoginManager()
login_manager.init_app(logout)

@logout.route('/logout')
@login_required
def show():
  if current_user.is_authenticated:
    log_logout(current_user)
    logout_user()
    return redirect(url_for('login.show') + '?success=logged-out')
  else:
    log_error(ip=request.remote_addr, error="logout-not-logged-in")
    return redirect(url_for('login.show') + '?error=not-logged-in')