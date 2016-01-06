from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("Home.html")




if __name__ == "__main__":
    app.debug == True
    app.secret_key = "k|5D5PH~21x1.zLg1r.Gj?9v"
    app.run('107.170.107.124',port=8000)
