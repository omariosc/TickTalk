from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app,db,login,logout,logs,models,register,room,settings
import unittest

class TestCase(unittest.TestCase):
  def setUp(self):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    self.app = app.test_client()
    pass

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    
  def test_load_login(self):
    response = self.app.get('/login',follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
  def test_load_register(self):
    response = self.app.get('/register',follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    
  def test_load_index(self):
    response = self.app.get('/',follow_redirects=True)
    self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
  unittest.main()