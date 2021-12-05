# Imports required modules
from flask import render_template, flash, request
from app import app
from .forms import CreateAssessment
from app import db, models

# Variables storing strings appearing more than once
home_description = 'You have no assessments.'
home_template = 'home.html'
home_title = 'All Assessments'
comp_description = 'You have not completed any assessments.'
completed_title = 'Completed Assessments'
completed_link = "/complete"
uncomp_description = 'Well Done! You have no uncompleted assessments.'
uncomplete_title = 'Uncompleted Assessments'
uncomplete_link = "/uncomplete"

# Functions to run flash mesage
def flash_unmark():
	flash('Successfully unmarked assessment.')
def flash_mark():
	flash('Successfully marked assessment as complete.')
def flash_delete():
	flash('Successfully deleted assessment.')

# Home page route
@app.route('/', methods=['GET'])
def home():
	# Sets home description
	description = home_description
	# Gets all tasks and sorts by id
	tasks = models.Assessment.query.order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		description = ''
	# Return the render template
	return render_template(home_template,title=home_title,description=description,tasks=tasks,link="")

# Home page route for marking task as complete
@app.route('/mark/<task_id>', methods=['GET'])
def mark(task_id):
	# Sets home description
	description = home_description
	# Sets task's status to completed
	models.Assessment.query.filter_by(id=task_id).update({"status": 1})
	# Commits update to database
	db.session.commit()
	# Gets all tasks and sorts by id
	tasks = models.Assessment.query.order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		description = ''
	flash_mark()
	# Return the render template
	return render_template(home_template,title=home_title,description=description,tasks=tasks,link="")

# Home page route for marking task as uncomplete
@app.route('/unmark/<task_id>', methods=['GET'])
def unmark(task_id):
	# Sets home description
	description = home_description
	# Sets task's status to uncomplete
	models.Assessment.query.filter_by(id=task_id).update({"status": 0})
	# Commits update to database
	db.session.commit()
	# Gets all tasks and sorts by id
	tasks = models.Assessment.query.order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		description = ''
	flash_unmark()
	# Return the render template
	return render_template(home_template,title=home_title,description=description,tasks=tasks,link="")

# Home page route for deleting task
@app.route('/delete/<task_id>', methods=['GET'])
def delete(task_id):
	# Sets home description
	description = home_description
	# Gets task by id
	task = models.Assessment.query.filter_by(id=task_id).one()
	# Deltes task from database
	db.session.delete(task)
	# Commits update to database
	db.session.commit()
	# Gets all tasks and sorts by id
	tasks = models.Assessment.query.order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		description = ''
	flash_delete()
	# Return the render template
	return render_template(home_template,title=home_title,description=description,tasks=tasks,link="")

# Create route for creating assessment
@app.route('/create', methods=['GET', 'POST'])
def create():
	# Creates form
	form = CreateAssessment()
	if form.validate_on_submit():
		# Creates task
		task = models.Assessment(title=form.title.data,code=form.code.data,deadline=form.deadline.data,description=form.description.data, status=0)
		# Adds task to database
		db.session.add(task)
		# Commits update to database
		db.session.commit()
		flash('Successfully created assessment.')
	# Return the render template
	return render_template('create.html',title='Create Assessments',form=form,task=0)

# Complete route for all completed tasks
@app.route('/complete', methods=['GET'])
def complete():
	# Sets description
	completed_description = comp_description
	# Gets completed tasks
	tasks = models.Assessment.query.filter_by(status=1).order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		completed_description = ''
	# Return the render template
	return render_template(home_template,title=completed_title,description=completed_description,tasks=tasks,link=completed_link)

# Complete unmark route for unmarking a task by id under complete assessments
@app.route('/complete/unmark/<task_id>', methods=['GET'])
def unmark_completed(task_id):
	# Sets description
	completed_description = comp_description
	# Marks task as uncomplete
	models.Assessment.query.filter_by(id=task_id).update({"status": 0})
	# Commits update to database
	db.session.commit()
	# Gets completed tasks
	tasks = models.Assessment.query.filter_by(status=1).order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		completed_description = ''
	flash_unmark()
	# Return the render template
	return render_template(home_template,title=completed_title,description=completed_description,tasks=tasks,link=completed_link)

# Complete delete route for deleting a task by id under complete assessments
@app.route('/complete/delete/<task_id>', methods=['GET'])
def delete_completed(task_id):
	# Sets description
	completed_description = comp_description
	# Gets task by id
	task = models.Assessment.query.filter_by(id=task_id).one()
	# Deletes task from database
	db.session.delete(task)
	# Commits update to database
	db.session.commit()
	# Gets all completed tasks
	tasks = models.Assessment.query.filter_by(status=1).order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		completed_description = ''
	flash_delete()
	# Return the render template
	return render_template(home_template,title=completed_title,description=completed_description,tasks=tasks,link=completed_link)

# Uncomplete route for showing uncomplete assessments
@app.route('/uncomplete', methods=['GET'])
def uncomplete():
	# Sets description
	uncomplete_description = uncomp_description
	# Gets all uncompleted tasks
	tasks = models.Assessment.query.filter_by(status=0).order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		uncomplete_description = ''
	# Return the render template
	return render_template(home_template,title=uncomplete_title,description=uncomplete_description,tasks=tasks,link=uncomplete_link)

# Uncomplete mark route for marking task as complete under uncomplete assessments
@app.route('/uncomplete/mark/<task_id>', methods=['GET'])
def mark_complete(task_id):
	# Sets description
	uncomplete_description = uncomp_description
	# Marks task as complete
	models.Assessment.query.filter_by(id=task_id).update({"status": 1})
	# Commits update to database
	db.session.commit()
	# Gets uncompleted tasks
	tasks = models.Assessment.query.filter_by(status=0).order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		uncomplete_description = ''
	flash_mark()
	# Return the render template
	return render_template(home_template,title=uncomplete_title,description=uncomplete_description,tasks=tasks,link=uncomplete_link)

# Uncomplete delete route for deleting task in uncomplete assessments
@app.route('/uncomplete/delete/<task_id>', methods=['GET'])
def delete_uncomplete(task_id):
	# Sets description
	uncomplete_description = uncomp_description
	# Gets task by id
	task = models.Assessment.query.filter_by(id=task_id).one()
	# Deletes task from database
	db.session.delete(task)
	# Commits update to database
	db.session.commit()
	# Gets all uncompleted tasks
	tasks = models.Assessment.query.filter_by(status=0).order_by(models.Assessment.id).all()
	# If there is at least one task, remove description
	if len(tasks) > 0 :
		uncomplete_description = ''
	flash_delete()
	# Return the render template
	return render_template(home_template,title=uncomplete_title,description=uncomplete_description,tasks=tasks,link=uncomplete_link)

# Edit route for editing route
@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit(task_id):
	# Gets task by id
	task = models.Assessment.query.filter_by(id=task_id).one()
	# Creates assessment form for editing
	form = CreateAssessment()
	if form.validate_on_submit():
		# Copies data from form to task
		task.title=form.title.data
		task.code=form.code.data
		task.deadline=form.deadline.data
		task.description=form.description.data
		# Commits update to database
		db.session.commit()
		flash('Successfully edited assessment.')
	# Return the render template
	return render_template('create.html',title='Edit Assessment',form=form,task=task)
