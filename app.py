from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask import request
from flask import jsonify
app = Flask(__name__)
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
    return jsonify(
        og_password = password,
        hash_password = pw_hash,
        result_comparion = result 
    )

@app.route('/user/<string:user>/<string:roll>/<string:age>',methods=["POST"])
def user(user,roll,age):
    username=user
    user=user_collection.insert_one({"name": username,"rollNo.":roll,"age":age})  
    return jsonify({
        "user": user
    })

    
    

if __name__ == '__main__':
    app.run()

