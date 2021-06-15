#from gpsposition_model import GpsPosition
from datetime import date, datetime
import json
from typing import List
import pprint
import pymongo
from bson import ObjectId, json_util
from flask import Flask, Response, request, jsonify, session
from geojson import Point
import uuid



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
    devicePhoneNumber: str
    ownerPhoneNumber: str
    #locations: List[GpsPosition]
    locations: List[str]

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
            "name": self.name,
            "imei": self.imei,
            "owner": self.owner,
            "devicePhoneNumber": self.devicePhoneNumber,
            "ownerPhoneNumber": self.ownerPhoneNumber,
            "locations": locs
        }

    def add_location(self, location):
        self.locations.append(location)




    def get_device_from_db(self, imei: int) :
        coll = db["devices"]
              
        device = coll.find_one({"imei": imei})  
        if device != None:
            return  jsonify(device),200
        return "No device found", 400    
           
       
       

    def add_device_to_db(self):
        json = request.json
        device = {
             "_id": uuid.uuid4().hex,
             "name": json["name"],  
             "imei": json["imei"],
             "owner": json["owner"],# Sesssion Daten abrufbar?: session["user"]
             "devicePhoneNumber": json["devicePhoneNumber"],
             "ownerPhoneNumber": json["ownerPhoneNumber"],
             "battery" : "0",
             "locations": []
        }
        try:
            coll = db['devices']
            if coll.find_one({"imei":device["imei"]}):
                return jsonify({"error:":"Device already exists"}),400
            
            coll.insert_one(device)
            return jsonify(device), 200
            
            
        except Exception as e:
            print("error")
            raise



    #def add_position_to_device(self, dev: Device, position: GpsPosition) -> bool:
     #   pass


   # def get_locations_from_db(self, dev: Device) -> List[GpsPosition]:
    #    pass


    def delete_device_from_db(self,imei: int):
        coll = db["devices"]
              
        device = coll.find_one({"imei": imei})  
        if device != None:
            coll.delete_one({"imei": imei})
            return "device succesfully deleted!",200
        return "No device to delete found", 400    
           
       
