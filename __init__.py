from flask import Flask, render_template, flash, request, url_for, session, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import datetime
from functools import wraps

from content_mgmt import Content
from dbconnect import connection

TOPIC_DICT = Content()


app = Flask(__name__)
app.secret_key = "asfd345treghstrg"

@app.route("/")
def homepage():
	return  render_template("main.html")

@app.route("/dashboard/")
def dashboard():
	return  render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)
	
	
@app.errorhandler(404)
def page_not_found(e):
	return  render_template("404.html")
	

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash("You need to login first")
			return redirect(url_for('login_page'))
			
	return wrap

	
@app.route("/logout/")
@login_required
def login():
	session.clear()
	flash("You have been logged out!")
	gc.collect()
	return redirect(url_for('homepage'))

	
@app.route("/login/", methods = ['GET','POST'])
def login_page():
	error = ''
	try:
		c, conn = connection()
		if request.method == "POST":
			data = c.execute("select * from users where username = (%s)", [thwart(request.form['username'])])
			
			#get the first record
			data = c.fetchone()[2]
			
			#check if password matches
			if sha256_crypt.verify(request.form['password'], data):
				session['logged_in'] = True
				session['username'] = request.form['username']
				
				flash("You are now logged in!")
				return redirect(url_for('dashboard'))
				
			else:
				error = "Invalid credentials, try again!"
		
		gc.collect()	
		
		return render_template("login.html", error=error)
		
	except Exception as e:
		error = "Invalid credentials, try again!"
		return  render_template("login.html", error = error)


class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=20)])
	email = TextField('Email Address', [validators.Length(min=8, max=50)])
	password = PasswordField('Password', [validators.Required(),validators.Length(min=6, max=30),
				validators.EqualTo('confirm', message="Password must match")])	
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Privacy Notice</a> (Last updated May 2016)', [validators.Required()])
		
@app.route("/register/", methods = ['GET','POST'])
def register_page():
	try:
		form = RegistrationForm(request.form)
		
		if request.method == "POST" and form.validate():
			username = form.username.data
			password = sha256_crypt.encrypt((str(form.password.data))) 
			email = form.email.data
			c, conn = connection()
			
			x = c.execute("select * from users where username = (%s)", [thwart(username)])
			
			if int(x) > 0:
				flash("username taken! Try another one!")
				return render_template('register.html', form=form)
			else:
				#get the date of registeration, use China time
				datenow = datetime.datetime.utcnow()
				
				c.execute("insert into users (username, password, email, regdate) values (%s,%s,%s,%s)", (thwart(username), thwart(password), thwart(email), datenow))
				conn.commit()
				
				flash("Thanks for registering!")
				c.close()
				conn.close()
				gc.collect()
				
				session['logged_in'] = True
				session['username'] = username
				
				return redirect(url_for('dashboard'))
		
		return render_template("register.html", form=form)
		
	except Exception as e:
		return(str(e))


		
	
if __name__ == "__main__":
	app.run()