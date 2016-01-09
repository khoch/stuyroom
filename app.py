from flask import Flask
application = Flask(__name__)

@application.route('/')
@application.route('/home')
def home():
	return "<h1> Hi </h1>"



if __name__ == "__main__":
    application.debug == True
    application.secret_key = "k|5D5PH~21x1.zLg1r.Gj?9v"
    application.run('107.170.107.124',port=8000)
