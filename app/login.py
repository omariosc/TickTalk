from flask import Blueprint,url_for,render_template,redirect,request
from flask_login import LoginManager,login_user,current_user
from werkzeug.security import check_password_hash
from app.models import db,Users
from app.logs import log_user_login,log_error

login=Blueprint('login',__name__,template_folder='/templates')
login_manager=LoginManager()
login_manager.init_app(login)

@login.route('/login',methods=['GET','POST'])
def show():
  if request.method=='POST':
    username=request.form['username']
    password=request.form['password']
    user=Users.query.filter_by(username=username).first()
    if user:
      if check_password_hash(user.password,password):
        login_user(user)
        log_user_login(user)
        return redirect(url_for('home.show')+ '?success=logged-in')
      else:
        log_error(user=user,ip=request.remote_addr,error="login-incorrect-password")
        return redirect(url_for('login.show') + '?error=incorrect-password')
    else:
      log_error(ip=request.remote_addr,error="login-user-not-found")
      return redirect(url_for('login.show') + '?error=user-not-found')
  else:
    return render_template('login.html',title="Login")
