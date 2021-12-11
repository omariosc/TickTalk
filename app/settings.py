# Import required modules
from flask import Blueprint,url_for,render_template,redirect,request,flash
from flask_login import LoginManager,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from app.models import db,Users
from app.logs import log_change_password,log_error

# Created settings blueprint
settings=Blueprint('settings',__name__,template_folder='/templates')
settings_manager=LoginManager()
settings_manager.init_app(settings)

# For url redirect
showtxt="settings.show"

# Login required to access settings
@settings.route('/settings',methods=['GET','POST'])
@login_required
def show():
  # If user changes password
  if request.method=='POST':
    # Gets values from form
    old_password=request.form['old_password']
    new_password=request.form['new_password']
    confirm_password=request.form['confirm_password']
    # If values exist
    if old_password and new_password and confirm_password:
      # If password is correct
      if check_password_hash(current_user.password,old_password):
        # If new passwords match
        if new_password==confirm_password:
          # Hashes password and updates password in database
          hashed_password=generate_password_hash(new_password,method='sha256')
          Users.query.filter_by(username=current_user.username).update({"password": hashed_password})
          db.session.commit()
          # Logs password change
          log_change_password(current_user)
          flash("Changed password")
          return redirect(url_for(showtxt) + '?success=changed-password')
        else:
          flash("Passwords do not match", "error")
          # If passwords dont match
          log_error(user=current_user,ip=request.remote_addr,error="passwords-dont-match")
          return redirect(url_for(showtxt) + '?error=passwords-dont-match')
      else:
        flash("Incorrect password", "error")
        # If incorrect password
        log_error(user=current_user,ip=request.remote_addr,error="incorrect-password")
        return redirect(url_for(showtxt) + '?error=incorrect-password')
    else:
      flash("Missing fields", "error")
      # If there were missing fields
      log_error(user=current_user,ip=request.remote_addr,error="missing-fields")
      return redirect(url_for(showtxt) + '?error=missing-fields')
  else:
    # Renders the settings template
    return render_template('settings.html',title="Settings")
