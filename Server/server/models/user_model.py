from geojson import Point
from flask import Flask, Response, request
import pymongo
import json
from bson import ObjectId, json_util


############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient("localhost:27017", serverSelectionTimeoutMS=1000)

    db = mongo.smts
   # mongo.server_info()

except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


####################### user class ########################
class User:
    id = ""
    name = ""
    surname = ""
    devices = []

    def get_user_as_dict(self):
        userd = {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "devices": self.devices
        }
        return userd
