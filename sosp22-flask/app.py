# import flask libraries
from flask import Flask, jsonify, request
app = Flask(__name__)

# flask run -> server runs at http://127.0.0.1:24000/ 
@app.route("/")
def hello():
    return "Hello World!"

# mock JSON database of some staff's favorite cats 
fav_cats = [
        {'Harsh': 'Indian Billi',
        {'Mon': 'Calico',
        {'Saurav': 'All cats!',
        {'Drshi': 'Maine Coons'}]


@app.route('/favcat', methods=['GET'])
def get_all_cats():
    # @TODO: get all the cat entries
    return jsonify()

@app.route('/favcat/<string:name>', methods=['GET'])
def get_one_cat(name):
    # @TODO: get only ONE cat entry
    return jsonify()

@app.route('/favcat', methods=['POST'])
def add_cat():
    # @TODO: add a staff and their favorite cat 
    return jsonify()

@app.route('/favecat/<string:name>', methods=['PUT'])
def edit_cat(name):
    # @TODO: modify an entry in JSON 
    return jsonify()

@app.route('/favcat/<string:name>', methods=['DELETE'])
def delete_cat(name):
    # @TODO: delete a staff :(
    return jsonify()