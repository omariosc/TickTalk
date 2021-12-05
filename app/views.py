# Imports required modules
from flask import render_template, flash, request
from app import app
from .forms import CreateAssessment
from app import db, models

# Home page route
@app.route('/', methods=['GET'])
def home():
	# Return the render template
	return render_template('home.html',title='Home')
