from flask import Flask, render_template, request, session, redirect, url_for
import json
import database

application = Flask(__name__)

@application.route('/')
@application.route('/cal')
def cal():
    #check if user is logged in
    if "loggedin" not in session:
        session["loggedin"] = False;
    return render_template("cal.html")

@application.route('/reserve', methods=['GET','POST'])
def reserve():
    room = ""
    if request.method == 'GET':
        room = request.args.get('rm')
        print room
    if request.method == 'POST':
        leadername = request.form['name']
        clubname = request.form['clubname']
        email = request.form['email']
        date = request.args.get('date')
        room = request.args.get('rm')
        #stores info in database
        database.addReservation(room, date, clubname, leadername, email)
        return redirect(url_for('cal'))
    return render_template("room.html", rm=room)


@application.route('/test')
def test():
    return render_template("rotest.html")

@application.route('/taken')
def taken():
    if request.method == 'GET':
        date = request.args.get("date");
        data = database.getTakenRooms(date)
    return json.dumps(data)

@application.route('/available')
def available():
    data = []
    if request.method == 'GET':
        date = request.args.get("date");
        data = database.getAvailableRooms(date)
    return json.dumps(data)


@application.route('/login', methods=['GET', 'POST'])
def login():
    if "loggedin" not in session:
        session["loggedin"] = False
    if session["loggedin"]:
        return redirect(url_for("home"))
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


@application.route("/changepass", methods=['GET', 'POST'])
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
    

@application.route("/home", methods=["GET","POST"])
def home():
	return render_template("home.html")

@application.route("/logout")
def logout():
    session["loggedin"] = False
    session['uname'] = ""
    return redirect(url_for("home"))

@application.route("/signup", methods=['GET', 'POST'])
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
            if database.addUser(uname, passw):
                return redirect(url_for("login"))
            else:
                return render_template("signup.html", NOTLOGGEDIN = "Error: Username already exists")

@application.route("/myaccount")
def myaccount():
    if 'loggedin' in session and 'user' in session and session["loggedin"]:
		return render_template("myaccount.html", LOGGEDIN = session['user'])
    else:
		return(render_template("myaccount.html"))

application.secret_key = "k|5D5PH~21x1.zLg1r.Gj?9v"
if __name__ == "__main__":
    

    application.run('0.0.0.0',port=8001)
