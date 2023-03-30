""" FLASK SERVER FOR WEB APP """
from flask import Flask, render_template, request
app = Flask(__name__)
app_version = '1.0'

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

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form.get('textbox') 
    print(f"New feedback received: {feedback}") 
    return render_template('feedback.html', feedback=feedback)