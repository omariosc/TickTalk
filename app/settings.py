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
          # Password should be at least 6 characters
          if len(new_password) < 6:
            flash("Password too short", "error")
            # Logs error
            log_error(ip=request.remote_addr,error="register-password-too-short")
            return redirect(url_for(showtxt) + '?error=password-too-short')
          # Password should be maximum 20 characters
          if len(new_password) > 20:
            flash("Password too long", "error")
            # Logs error
            log_error(ip=request.remote_addr,error="register-password-too-long")
            return redirect(url_for(showtxt) + '?error=password-too-long')
          #If new password is different from the old password]
          if check_password_hash(current_user.password,new_password) == False:
            # Hashes password and updates password in database
            hashed_password=generate_password_hash(new_password,method='sha256')
            Users.query.filter_by(username=current_user.username).update({"password": hashed_password})
            db.session.commit()
            # Logs password change
            log_change_password(current_user)
            flash("Changed password")
            return redirect(url_for(showtxt) + '?success=changed-password')
          else:
            flash("New password cannot be same as old password", "error")  
            # If passwords dont match
            log_error(user=current_user,ip=request.remote_addr,error="settings-same-password")
            return redirect(url_for(showtxt) + '?error=same-password')
        else:
          flash("Passwords do not match", "error")
          # If passwords dont match
          log_error(user=current_user,ip=request.remote_addr,error="settings-passwords-dont-match")
          return redirect(url_for(showtxt) + '?error=passwords-dont-match')
      else:
        flash("Incorrect password", "error")
        # If incorrect password
        log_error(user=current_user,ip=request.remote_addr,error="settings-incorrect-password")
        return redirect(url_for(showtxt) + '?error=incorrect-password')
    else:
      flash("Missing fields", "error")
      # If there were missing fields
      log_error(user=current_user,ip=request.remote_addr,error="settings-missing-fields")
      return redirect(url_for(showtxt) + '?error=missing-fields')
  else:
    # Renders the settings template
    return render_template('settings.html',title="Settings")
