from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from TweetsExtractor import *
import json
import pickle
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'bigfiveUser'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/bigfiveUser'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

@app.route('/register', methods=['POST', 'GET'])
def register():
    users = mongo.db.users
    uname = request.get_json()['uname']
    # print (first_name)
    email = request.get_json()['email']
    contact = request.get_json()['contact']
    gender = request.get_json()['gender']
    age = request.get_json()['age']
    password = bcrypt.generate_password_hash(request.get_json()['psw']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
        'uname': uname,
        'email': email,
        'conatct' : contact,
        'age': age,
        'gender': gender,
        'password' : password,
        'created'  :created
    })

    new_user = users.find_one({'_id': user_id})

    result = {'uname': new_user['uname'] + " registered"}

    return jsonify({'result': uname})

@app.route('/login', methods=['POST', 'GET'])
def login():
    users = mongo.db.users
    uname = request.get_json()['uname']
    password = request.get_json()['psw']
    result = ""

    response = users.find_one({'uname': uname})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
                'email': response['email'],
                'contact': response['contact'],
                # 'email': response['email']
            })
            result = jsonify({"token": access_token})
        else:
            result = jsonify({"error": "Invalid username or password"})
    else:
        result = jsonify({"result": "No result found"})
    return result

@app.route('/twitterID', methods=['POST', 'GET'])
def postTwitterID():
    #users = mongo.db.users
    twitterID = request.get_json()['twitterID']
    print (twitterID)
    i = PersonalityInsights()
    recommendations = i.watsonSubmission(i.pullTweets(twitterID), twitterID) 
    data = {}
    index = 0
    for i in range(0, 5):
        for r in recommendations[i]:
            data[r['url']] = r['title']
            json_data = json.dumps(data)
            print(r['title'])
            index+=1

    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)


