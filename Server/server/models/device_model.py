#from gpsposition_model import GpsPosition
import re
import pymongo
from flask import jsonify, session, request
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


def check_against_userID(id_to_check:str):
    if "logged_in" in session and session["user"]["_id"]==id_to_check:
        return True
    return False

class Device:
    def add_location(self, location):
        self.locations.append(location)

    def get_device_from_db(self, imei: str):
        coll = db["devices"]

        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            del device["locations"]
            if device != None:
                   return jsonify(device), 200
        return jsonify({"error":"No device found"}), 400

    def add_device_to_db(self):
        json = request.json
        device = {
            "_id": uuid.uuid4().hex,
            "name": json["name"],
            "imei": json["imei"],
            # "owner": json["owner"],# Sesssion Daten abrufbar?: session["user"]
            "owner": session["user"]["_id"],
            "devicePhoneNumber": json["devicePhoneNumber"],
            "ownerPhoneNumber": session["user"]["phoneNumber"],
            "battery": 0.0,
            "locations": []
        }
        try:
            device_coll = db['devices']
            user_coll = db['users']
            if device_coll.find_one({"imei": device["imei"]}):
                return jsonify({"error:": "Device already exists"}), 400

            device_coll.insert_one(device)
            user_coll.update_one({"_id": session["user"]["_id"]}, {"$push": {"devices":device["imei"]}})
            return jsonify(device_coll.find_one({"imei":json["imei"]})), 200

        except Exception as e:
            print("error")
            raise

    def add_position_to_device(self, imei: str):
        coll = db["devices"]
        json_list = request.json
        position_list = []
        device = coll.find_one({"imei":imei})
        if device!=None and check_against_userID(device["owner"]):
            for json in json_list:
                coll.update_one({"imei": imei}, {"$push": {"locations":json}})

            return jsonify({"message":"position added to device"}), 200

        return jsonify({"error":"No device to add location to"}), 404

    def delete_locations(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            coll.update_one({"imei": imei}, {"$set": {"locations":[]}})
            return jsonify({"message":"locations deleted"}), 200
        return jsonify({"error":"not possible to delete locations"}), 400

    def get_locations_from_db(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            locations = device.get('locations')

            return jsonify(locations), 200
        return jsonify({"error":"No device to get locations from"}), 400

    def delete_device_from_db(self, imei: str):
        devices_coll = db["devices"]
        user_coll = db["users"]
        device = devices_coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            
            devices_coll.delete_one({"imei": imei})
            user_coll.update_one({"_id": session["user"]["_id"]}, {"$pull": {"devices":device["imei"]}})
            return jsonify({"message":"device succesfully deleted!"}), 200
        return jsonify({"error":"you dont own a device with the imei "+imei}), 400