from flask import Flask, render_template

application = Flask(__name__)

@application.route('/')
@application.route('/home')
def home():
	return '''
<h1> Hello World </h1>
<a href="/cal"> Calendar </a>

<a href="/test"> Test </a> 
'''

@application.route('/cal')
def cal():
    return render_template("templates/cal.html")

@application.route('/test')
def test():
    return render_template("templates/test.html")

if __name__ == "__main__":
    application.debug == True
    application.secret_key = "k|5D5PH~21x1.zLg1r.Gj?9v"
    application.run('0.0.0.0',port=8000)
