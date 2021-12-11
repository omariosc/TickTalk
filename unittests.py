from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app,login,logout,logs,models,register,room,settings
import os, unittest

class TestCase(unittest.TestCase):
  def setUp(self):
    app.config.from_object('config')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    self.app = app.test_client()
    models.db.create_all()
    pass

  def tearDown(self):
    models.db.session.remove()
    models.db.drop_all()
    
  def test_addtaskroute(self):
    response = self.app.get('/add_task',follow_redirects=True)
    self.assertEqual(response.status_code, 200)
  