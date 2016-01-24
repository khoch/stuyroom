from flask import Flask, render_template, request, session, redirect, url_for
import json
#import database

application = Flask(__name__)

@application.route('/')
@application.route('/home')
def home():
	return render_template("home.html")

@application.route('/cal')
def cal():
    return render_template("cal.html")

@application.route('/reserve', methods=['GET','POST'])
def reserve():
    if request.method == 'POST':
         leadername = request.form['name']
         clubname = request.form['clubname']
         email = request.form['email']
         room = request.args.get('rm')
         date = request.args.get('date')
         #database.addReservation(room, date, clubname, leadername, email)
         return redirect(url_for('cal'))
    return render_template("room.html")


@application.route('/test')
def test():
    return render_template("rotest.html")

@application.route('/taken')
def taken():
        if request.method == 'GET':
                #data = database.getTakenRooms(date)
                data = [[555, "smash bros"],[555, "jsa"],[555, "key club"],[555,"history club"]]
        return json.dumps(data)

@application.route('/available')
def available():
        data = []
        if request.method == 'GET':
                date = request.args.get("date");
                #data = database.getAvailableRooms(date)
                data = [229,231,303,313,315,327,329,333,335,337,339,403,404,405,407,427,437,431]
        return json.dumps(data)

if __name__ == "__main__":
    application.debug = True
   # application.secret_key = "k|5D5PH~21x1.zLg1r.Gj?9v"
    application.run('0.0.0.0',port=8000)
