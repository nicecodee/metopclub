from flask import Flask, render_template, flash, redirect

app = Flask(__name__)
app.secret_key = "asfd345treghstrg"

@app.route("/")
def homepage():
    return  render_template("main.html")

@app.route("/dashboard/")
def dashboard():
	flash('good')
	return  render_template("dashboard.html")
	
	
@app.errorhandler(404)
def page_not_found(e):
	return  render_template("404.html")
	
	
if __name__ == "__main__":
    app.run()