from flask import Flask, render_template, request, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
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
        hashedPassword = pbkdf2_sha256.encrypt(passw, rounds=20000, salt_size=16)
        #button = request.form['button']
	if database.checkUser(uname, hashedPassword) == 0:
            session["loggedin"] = True
            session['user'] = uname
            return redirect(url_for("adminhome"))
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
        oldPasswordHashed = pbkdf2_sha256.encrypt(oldpassw, rounds=20000, salt_size=16)
        if database.checkUser(uname, oldPasswordHashed) == 0:
            if newpassw1 != newpassw2:
                return render_template("changepass.html", ERROR = "Error: New passwords do not match.")
            newPasswordHashed = pbkdf2_sha256.encrypt(newpassw1, rounds=20000, salt_size=16)
            database.changePassword(uname, newPasswordHashed)
            return redirect(url_for("login"))
        else:
            return render_template("changepass.html", ERROR = "Error: Wrong username or password.")
    

@app.route("/adminhome", methods=["GET","POST"])
def adminhome():
	return render_template("adminhome.html")

@app.route("/logout")
def logout():
    session["loggedin"] = False
    session['uname'] = ""
    return redirect(url_for("adminhome"))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if not'loggedin' in session or not session["loggedin"]:
        return render_template("adminhome.html")
    if request.method=="GET":
        return render_template("signup.html")
    else:
        if request.form['pass'] != request.form['confirmpass']:
            return render_template("signup.html", ERROR = "Error: 'Password' and 'Confirm Password' do not match.")
        elif len(request.form['user']) < 4 or len(request.form['pass']) < 8:
            return render_template("signup.html", ERROR = "Error: 'Username' must be at least 4 characters and 'Password' must be at least 8 characters.")
        else: 
            uname = request.form['user']
            passw = request.form['pass']
            #button = request.form['button']
            usernameHashed = pbkdf2_sha256.encrypt(uname, rounds=20000, salt_size=16)
            passwordHashed = pbkdf2_sha256.encrypt(passw, rounds=20000, salt_size=16)			
            if database.addUser(usernameHashed, passwordHashed):
                return redirect(url_for("login"))
            else:
                return render_template("signup.html", ERROR = "Error: Username already exists")

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
    
