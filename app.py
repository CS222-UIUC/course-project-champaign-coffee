""" FLASK SERVER FOR WEB APP """
from flask import Flask, render_template
app = Flask(__name__)
""" type 'flask run' in terminal to run local server to http://127.0.0.1:5000/ """

@app.route("/")
def home():
    """ default server """
    return render_template('index.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

@app.route('/ratings')
def ratings():
    return render_template('ratings.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
