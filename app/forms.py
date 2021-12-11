# Imports required modules
from flask_wtf import Form
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired,Length,Regexp,Email

# Form for registering user
class RegisterUser(Form):
  username=StringField('username',validators=[DataRequired(),Length(max=20),Regexp(r"^[a-zA-Z0-9_]*$")])
  email=StringField('email',validators=[DataRequired(),Length(max=50),Email()])
  password=StringField('password',validators=[DataRequired(),Length(min=6,max=20),Regexp(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,20}$")])
  confirm_password=StringField('confirm_password',validators=[DataRequired(),Length(max=20),Regexp(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,20}$")])

# Form for user logging in
class LoginUser(Form):
  username=StringField('username',validators=[DataRequired(),Length(max=20)])
  password=StringField('password',validators=[DataRequired(),Length(min=6,max=20)])

# Form for changing password
class ChangePassword(Form):
  old_password=StringField('old_password',validators=[DataRequired(),Length(min=6,max=20)])
  new_password=StringField('new_password',validators=[DataRequired(),Length(min=6,max=20),Regexp(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,20}$")])
  confirm_password=StringField('confirm_password',validators=[DataRequired(),Length(max=20),Regexp(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,20}$")])

# Form for sending message
class SendMessage(Form):
  message=StringField('message',validators=[DataRequired(),Length(max=200)])
