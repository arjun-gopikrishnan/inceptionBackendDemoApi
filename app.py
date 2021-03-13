from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask import request
from flask import jsonify
import json
# from mongoengine import MongoEngineJSONEncoder
# from mongoengine.base import BaseDocument
app = Flask(__name__)
# app.json_encoder = MongoEngineJSONEncoder
import db
from db import *
api = Api(app)
bcrypt = Bcrypt(app)


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
    user_collection.insert_one({"name": username,"rollNo":roll,"age":age}).inserted_id
    return jsonify({
        "message": 'data entered into database'
    })

@app.route('/return',methods=["GET"])
def getAll():    
    res = {}
    for x in user_collection.find():              
      res['DB response'] = x
      print(x)



    return jsonify('check console')



    

if __name__ == '__main__':
    app.run(debug=True,port=3000,host='0.0.0.0')

