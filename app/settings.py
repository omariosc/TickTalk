from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Users
from app.logs import log_change_password

settings = Blueprint('settings', __name__, template_folder='/templates')
settings_manager = LoginManager()
settings_manager.init_app(settings)
showtxt = "settings.show"

@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def show():
  if request.method == 'POST':
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    user = Users.query.filter_by(username=current_user.username).first()
    if user != 0:
      if old_password and new_password and confirm_password:
        if check_password_hash(user.password, old_password):
          if new_password == confirm_password:
            hashed_password = generate_password_hash(new_password, method='sha256')
            Users.query.filter_by(username=current_user.username).update({"password": hashed_password})
            db.session.commit()
            log_change_password(current_user)
            return redirect(url_for(showtxt) + '?success=changed-password')
          else:
            return redirect(url_for(showtxt) + '?error=password-dont-match')
        else:
          return redirect(url_for(showtxt) + '?error=incorrect-password')
      else:
        return redirect(url_for(showtxt) + '?error=missing-fields')
    else:
      return redirect(url_for(showtxt) + '?error=user-not-found')
  else:
    return render_template('settings.html', title="Settings")
