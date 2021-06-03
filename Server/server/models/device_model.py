from datetime import date, datetime
import json
from typing import List

import pymongo
from bson import ObjectId, json_util
from flask import Flask, Response, request
from geojson import Point

from gpsposition_model import gpsPosition

############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient(
        "localhost:27017",
        serverSelectionTimeoutMS=1000)

    db = mongo.smts
   # mongo.server_info()

except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


class Device:
    name: str
    imei: int
    owner: int
    devicePhoneNumber: int
    ownerPhoneNumber: int
    locations: List[gpsPosition]

    def __init__(self, name="", imei=0, owner=0,
                 devicePhoneNumber=0, ownerPhoneNumber=0):
        self.name = name
        self.imei = imei
        self.owner = owner
        self.devicePhoneNumber = devicePhoneNumber
        self.ownerPhoneNumber = ownerPhoneNumber
        self.locations = []

    def as_dict(self):
        locs = []
        
        for loc in self.locations:
            locs.append(loc.as_dict())
        
        return {
            "Name": self.name,
            "IMEI": self.imei,
            "owner": self.owner,
            "devicePhoneNumber": self.devicePhoneNumber,
            "ownerPhoneNumber" : self.ownerPhoneNumber,
            "locations": locs
        }


    def add_location(self, location):
        self.locations.append(location)
        

def add_device_to_db(device:Device):
    try:
        coll = db['devices']
        dict_device = device.as_dict()
        json_as = json.dumps(dict_device)
        result = coll.insert_one(dict_device).inserted_id
        
        return result
    except Exception as e:
        print("error")
        raise


