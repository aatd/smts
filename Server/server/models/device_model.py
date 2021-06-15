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
from models.gpsposition_model import GpsPosition




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
    


    def add_location(self, location):
        self.locations.append(location)




    def get_device_from_db(self, imei: str):
        coll = db["devices"]
              
        device = coll.find_one({"imei": imei})
        del device["locations"]  
        if device != None:
            return  jsonify(device),200
        return "No device found", 400    
           
       
       

    def add_device_to_db(self):
        json = request.json
        device = {
             "_id": uuid.uuid4().hex,
             "name": json["name"],  
             "imei": json["imei"],
             #"owner": json["owner"],# Sesssion Daten abrufbar?: session["user"]
             "owner": session["user"]["name"],
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



    def add_position_to_device(self, imei: str):
        coll = db["devices"]
        json = request.json
        gpsPos = {
            "latitude" :  json["latitude"],
            "longitude" : json["longitude"],
            "height" : json["height"],
            "time" : json["time"],
            "velocity" : json["velocity"]
        }
        
        device = coll.find_one({"imei":imei})
        if device != None:
            device.get('locations').append(gpsPos)
            coll.find_one_and_replace({"imei": imei}, device)
        
            return jsonify(gpsPos),200
        return "No device to add location to", 404   

    def delete_locations(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei":imei})
        if device != None:
            del device.get('locations')[:]
            coll.find_one_and_replace({"imei":imei}, device)
            return "locations deleted", 200    

        
            


    def get_locations_from_db(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None:
            locations = device.get('locations')
            
           
            
           
            return jsonify(locations)
        return "No device to get locations from",400    


    def delete_device_from_db(self,imei: str):
        coll = db["devices"]
              
        device = coll.find_one({"imei": imei})  
        if device != None:
            coll.delete_one({"imei": imei})
            return "device succesfully deleted!",200
        return "No device to delete found", 400    
           
       
