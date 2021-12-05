# Imports required modules
from flask_wtf import Form
from wtforms.fields.core import StringField
from wtforms.fields.html5 import DateField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length

# Form containing fields for assessment
class CreateAssessment(Form):
  # Title uses StringField with max length of 100 characters and must contain a value
  title = StringField('title', validators=[DataRequired(), Length(max=100)])
  # Module Code uses StringField with max length of 10 characters and must contain a value
  code = StringField('code', validators=[DataRequired(), Length(max=10)])
  # Deadline uses DateField, does not need validators as DateField from html5 validates this already
  deadline = DateField('deadline')
  # Description uses TextAreaField with max length of 500 characters and must contain a value
  description = TextAreaField('description', validators=[DataRequired(), Length(max=500)])
