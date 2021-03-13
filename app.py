
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask import request
from flask import jsonify
import json
import ast


# from mongoengine import MongoEngineJSONEncoder
# from mongoengine.base import BaseDocument
app = Flask(__name__)
# app.json_encoder = MongoEngineJSONEncoder
import db
from db import *
api = Api(app)
bcrypt = Bcrypt(app)
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
def hello():
    return "Welcome to inception 5.0"

@app.route('/test',methods=["POST"])
def test():
    password = request.args.get('password')
    pw_hash = bcrypt.generate_password_hash(password)
    result = bcrypt.check_password_hash(pw_hash,password)
    print(password,pw_hash,result)
    return jsonify(
        og_password = password,
        #hash_password = pw_hash,
        result_comparion = result 
    )

@app.route('/user/<string:user>/<string:roll>/<string:age>',methods=["POST"])
def user(user,roll,age):
    username=user
    user_collection.insert_one({"name": username,"rollNo":roll,"age":age})
    return jsonify({
        "message": 'data entered into database'
    })

@app.route('/return',methods=["GET"])
def getAll():    
    res = {}
    for x in user_collection.find():              
      var = JSONEncoder().encode(str(x))
      print((var))

    print('Last value of var',var)

    return jsonify(var)

@app.route('/login',methods=["POST"])
def login():
    data = request.data
    dict_str = data.decode("UTF-8")
    resData = ast.literal_eval(dict_str)
    
    #username = resData["user"]
    regNo = resData["rollNo"]
    userName = resData["name"]

    result = (user_collection.find_one({"name" : userName}))

    return jsonify(str(result))



    

if __name__ == '__main__':
    app.run(debug=True,port=3000,host='0.0.0.0')