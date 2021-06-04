import json

import pymongo
from bson import ObjectId, json_util
from flask import Flask, Response, request
from geojson import Point

############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient("localhost:27017", serverSelectionTimeoutMS=1000)

    db = mongo.smts
   # mongo.server_info()

except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


####################### user class ########################
class User:
    id = int
    name = str
    password = str
    phoneNumber = int
    devices = [int] # Listenelemente festlegen?
    

    def __init__(self, id=0, name="", password="",phoneNumber=0 ):
        self.id = id
        self.name = name
        self.password = password
        self.phoneNumber = phoneNumber
        self.devices = []

    def get_user_as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.surname,
            "phoneNumber": self.phoneNumber,
            "devices": self.devices
        }
def add_user_to_db(user:User):
    try:
        coll = db['users']
        dict_user = user.get_user_as_dict()
        json_as = json.dumps(dict_user)
        result = coll.insert_one(dict_user).inserted_id

        reutn result
    except Exception as e:
        print ("error")
        raise         
