from flask import Flask, render_template, flash, redirect, request, session


app = Flask(__name__)
app.secret_key = "asfd345treghstrg"

@app.route("/")
def homepage():
	return  render_template("main.html")

@app.route("/dashboard/")
def dashboard():
	flash('dashboard flash test')
	return  render_template("dashboard.html")
	
	
@app.errorhandler(404)
def page_not_found(e):
	return  render_template("404.html")
	

@app.route("/login/", methods = ['GET','POST'])
def login_page():
	return  render_template("login.html")
	
	
if __name__ == "__main__":
	app.run(debug = True)