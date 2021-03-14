
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask import request
from flask import jsonify,make_response
import json
import ast
import jwt

from datetime import datetime, timedelta 

from functools import wraps

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

import db
from db import *
api = Api(app)
bcrypt = Bcrypt(app)
from bson import ObjectId

app.config['SECRET_KEY'] = 'usersJWTsecretkEy'

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
def hello():
    return 'Welcome to inception 5.0'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing !!'}),401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_collection.find_one({"email" :  data["public_id"]})
        except:
            return jsonify({ 
                'message' : 'Token is invalid !!'
            }), 401 
        return  f(current_user, *args, **kwargs) 
   
    return decorated 

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

@app.route('/user/<string:email>/<string:password>/<string:name>',methods=["POST"])
def user(email,password,name):
    hashed_pass = bcrypt.generate_password_hash(password)
    user_collection.insert_one({"email": email,"password":hashed_pass,"name":name})
    return jsonify({
        "message": 'data entered into database'
    })

@app.route('/return',methods=["GET"])
@token_required
def getAll(current_user):    
    for x in user_collection.find():              
      var = JSONEncoder().encode(str(x))
      #print((var))

    # token = request.headers['x-access-token']
    # data = jwt.decode(token, app.config['SECRET_KEY'])
    # current_user = user_collection.find_one({"email" :  data["public_id"]})
    

    return jsonify(var)

@app.route('/login',methods=["POST"])
def login():
    data = request.data
    dict_str = data.decode("UTF-8")
    resData = ast.literal_eval(dict_str)
    
    password = resData["password"]
    userName = resData["email"]

    userAcc = (user_collection.find_one({"email" : userName}))
    
    if not userAcc:
        return jsonify("Account doesn't exist")
    result = bcrypt.check_password_hash(userAcc["password"],password)

    if result:
        token = jwt.encode({
            'public_id' : userAcc["email"],
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    else:
        return make_response( 
        'Could not verify', 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
    ) 



    

if __name__ == '__main__':
    app.run(debug=True,port=3000,host='0.0.0.0')