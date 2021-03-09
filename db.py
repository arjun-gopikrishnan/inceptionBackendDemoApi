from flask import Flask
import pymongo

app=Flask(__name__)

# CONNECTION_STRING = "mongodb+srv://swarnabha:swarnabhaflask@cluster0.sbgtv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
CONNECTION_STRING = "mongodb://localhost:27017/userDb"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('userDb')
user_collection = pymongo.collection.Collection(db, 'usersColl')