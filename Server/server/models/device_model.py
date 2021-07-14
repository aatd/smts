import pymongo
from flask import jsonify, session, request
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


def check_against_userID(id_to_check: str):
    if "logged_in" in session and session["user"]["_id"] == id_to_check:
        return True
    return False


class Device:

    # /devices
    def add_device_to_db(self):
        json = request.json
        device = {
            "_id": uuid.uuid4().hex,
            "name": json["name"],
            "imei": json["imei"],
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
                return jsonify({"error:": "Device already exists"}), 409

            device_coll.insert_one(device)
            user_coll.update_one({"_id": session["user"]["_id"]}, {
                                 "$push": {"devices": device["imei"]}})
            # return jsonify(device_coll.find_one({"imei":json["imei"]})), 201
            return jsonify({"message": "Device created"}), 201
        except Exception as e:
            return jsonify({"error": "could not create device"}), 400
            raise

    # /devices/{imei}

    def get_device_from_db(self, imei: str):
        coll = db["devices"]

        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            del device["locations"]
            if device != None:
                return jsonify(device), 200
        return jsonify({"error": "No device found"}), 400

    def delete_device_from_db(self, imei: str):
        devices_coll = db["devices"]
        user_coll = db["users"]
        device = devices_coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):

            devices_coll.delete_one({"imei": imei})
            user_coll.update_one({"_id": session["user"]["_id"]}, {
                                 "$pull": {"devices": device["imei"]}})
            return jsonify({"message": "device succesfully deleted!"}), 200
        return jsonify({"error": "you dont own a device with the imei "+imei}), 404

    # /devices/{IMEI}/locations
    def add_position_to_device(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if request.json != None:
            json_list = request.json
            coll.update_one({"imei": imei}, {"$push": {"locations": json_list}})

            return jsonify({"message": "position added to device"}), 200

        return jsonify({"error": "No device to add location to"}), 404

    def get_locations_from_db(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None: #and check_against_userID(device["owner"]):
            locations = device.get('locations')

            return jsonify(locations[len(locations)-1]), 200
        return jsonify({"error": "No device to get locations from"}), 404

    def delete_locations(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            coll.update_one({"imei": imei}, {"$set": {"locations": []}})
            return jsonify({"message": "locations deleted"}), 200
        return jsonify({"error": "not possible to delete locations"}), 400
