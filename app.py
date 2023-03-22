""" FLASK SERVER FOR WEB APP """
from flask import Flask, render_template
app = Flask(__name__)
""" type 'flask run' in terminal to run local server to http://127.0.0.1:5000/ """
@app.route("/")
def hello():
    """ default server """
    return render_template('index.html')
