from flask import Flask, render_template, request, session, redirect, url_for, es


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
         #call db function to store this info
         #return render_template succes message
         return render_template("room.html")


@application.route('/test')
def test():
    return render_template("rotest.html")

if __name__ == "__main__":
    application.debug = True
   # application.secret_key = "k|5D5PH~21x1.zLg1r.Gj?9v"
    application.run('0.0.0.0',port=8000)
