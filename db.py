from flask import Flask
import pymongo
import os
app=Flask(__name__)

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('userDb')
user_collection = pymongo.collection.Collection(db, 'usersColl')
user_collection.create_index( [("Username", pymongo.TEXT), ("Email", pymongo.ASCENDING)],unique=True)