# Imports database
from app import db

# Sets database for assessments
class Assessment(db.Model):
  # Id column primary key
  id = db.Column(db.Integer, primary_key=True)
  # Title column is string with maximum length of 100 characters
  title = db.Column(db.String(100))
  # Module Code column is string with maximum length of 10 characters
  code = db.Column(db.String(10))
  # Deadline column is of type date
  deadline = db.Column(db.Date())
  # Description column is string with maximum length of 500 characters
  description = db.Column(db.String(500))
  # Status column is of type Boolean
  status = db.Column(db.Boolean())
