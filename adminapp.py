from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import csv
import database

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])

@app.route("/login", methods=['GET', 'POST'])
def login():
    if "loggedin" not in session:
        session["loggedin"] = False
    if request.method=="GET":
        return render_template("login.html")
    else:
        uname = request.form['user']
        passw = request.form['pass']
        #button = request.form['button']
	if database.checkUser(uname, passw) == 0:
            session["loggedin"] = True
            session['user'] = uname
            return redirect(url_for("home"))
        else:
            return render_template("login.html", NOTLOGGEDIN = "Error: Wrong username or password.")  

@app.route("/changepass", methods=['GET', 'POST'])
def changepass():
    if "loggedin" not in session:
        session["loggedin"] = False
    if request.method=="GET":
        return render_template("changepass.html")
    else:
        uname = request.form['user']
        oldpassw = request.form['oldpass']
        newpassw1 = request.form['newpass1']
        newpassw2 = request.form['newpass2']
        #button = request.form['button']
        if database.checkUser(uname, oldpassw) == 0:
            if newpassw1 != newpassw2:
                return render_template("changepass.html", ERROR = "Error: New passwords do not match.") 
            database.changePassword(uname, newpassw1)
            return redirect(url_for("login"))
        else:
            return render_template("changepass.html", ERROR = "Error: Wrong username or password.")
    

@app.route("/home", methods=["GET","POST"])
def home():
	return render_template("home.html")

@app.route("/logout")
def logout():
    session["loggedin"] = False
    session['uname'] = ""
    return redirect(url_for("home"))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        if request.form['pass'] != request.form['confirmpass']:
            return render_template("signup.html", NOTLOGGEDIN = "Error: 'Password' and 'Confirm Password' do not match.")
        elif len(request.form['user']) < 4 or len(request.form['pass']) < 8:
            return render_template("signup.html", NOTLOGGEDIN = "Error: 'Username' must be at least 4 characters and 'Password' must be at least 8 characters.")
        else: 
            uname = request.form['user']
            passw = request.form['pass']
            #button = request.form['button']			
            if database.addUser(uname, passw):
                return redirect(url_for("login"))
            else:
                return render_template("signup.html", NOTLOGGEDIN = "Error: Username already exists")

@app.route("/myaccount")
def myaccount():
    if 'loggedin' in session and 'user' in session and session["loggedin"]:
		return render_template("myaccount.html", LOGGEDIN = session['user'])
    else:
		return(render_template("myaccount.html"))


if __name__== "__main__":
    app.debug = True
    app.secret_key = "Password"
    app.run(host='0.0.0.0',port=8000)
    
