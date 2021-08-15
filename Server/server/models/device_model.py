import datetime
import uuid
from pprint import pprint

import pymongo
from flask import jsonify, request, session

##############################################
# Init DB
try:
    mongo = pymongo.MongoClient("localhost:27017", serverSelectionTimeoutMS=1000)
    db = mongo.smts
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
            "locations": [],
        }
        try:
            device_coll = db["devices"]
            user_coll = db["users"]
            if device_coll.find_one({"imei": device["imei"]}):
                return jsonify({"error:": "Device already exists"}), 409

            device_coll.insert_one(device)
            user_coll.update_one(
                {"_id": session["user"]["_id"]}, {"$push": {"devices": device["imei"]}}
            )
            # return jsonify(device_coll.find_one({"imei":json["imei"]})), 201
            return jsonify({"message": "Device created"}), 201
        except Exception as e:
            return jsonify({"error": "could not create device"}), 400
            raise

    # /devices
    def create_device(self, name, imei, devicePhoneNumber):
        device = {
            "_id": uuid.uuid4().hex,
            "name": name,
            "imei": imei,
            "owner": session["user"]["_id"],
            "devicePhoneNumber": devicePhoneNumber,
            "ownerPhoneNumber": session["user"]["phoneNumber"],
            "battery": 0.0,
            "locations": [],
        }
        try:
            device_coll = db["devices"]
            user_coll = db["users"]
            if device_coll.find_one({"imei": device["imei"]}):
                return jsonify({"error:": "Device already exists"}), 409

            device_coll.insert_one(device)
            user_coll.update_one(
                {"_id": session["user"]["_id"]}, {"$push": {"devices": device["imei"]}}
            )
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
            return device, 200
        return jsonify({"error": "No device found"}), 400

    def delete_device_from_db(self, imei: str):
        devices_coll = db["devices"]
        user_coll = db["users"]
        device = devices_coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):

            devices_coll.delete_one({"imei": imei})
            user_coll.update_one(
                {"_id": session["user"]["_id"]}, {"$pull": {"devices": device["imei"]}}
            )
            return jsonify({"message": "device succesfully deleted!"}), 200
        return jsonify({"error": "you dont own a device with the imei " + imei}), 404

    def get_device_status(self, imei):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device is not None and check_against_userID(device["owner"]):
            locations = device.get("locations")
            now = datetime.datetime.now()
            last_entry = locations[len(locations) - 1]["time"]
            maxDelta = datetime.timedelta(days=1)
            if now - last_entry > maxDelta:
                return jsonify("stolen"), 200
            else:
                return jsonify("not stolen"), 200

        return jsonify("device not found"), 404

    # /devices/{IMEI}/locations
    def add_position_to_device(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})

        if request.json != None and device != None:
            json_list = request.json

            # convert timestring into time.isoformat
            year = 2000 + int(json_list["time"][1:3])
            month = int(json_list["time"][4:6])
            day = int(json_list["time"][7:9])
            h = int(json_list["time"][10:12])
            m = int(json_list["time"][13:15])
            s = int(json_list["time"][16:18])
            ms = int(json_list["time"][19:21])
            time = datetime.datetime(year, month, day, h, m, s, ms)

            json_list["time"] = time

            res = coll.update_one({"imei": imei}, {"$push": {"locations": json_list}})

            return jsonify({"message": "position added to device"}), 200

        return jsonify({"error": "No device to add location to"}), 404

    def get_locations_from_db(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})

        if device != None:
            locations = device.get("locations")
            # if url parameters start and end are given -> only return locations in this period
            if request.args.get("start"):

                retLocations = []

                startTime = datetime.datetime.fromisoformat(request.args.get("start"))
                endTime = datetime.datetime.now()
                if request.args.get("end"):
                    endTime = datetime.datetime.fromisoformat(request.args.get("end"))
                for loc in locations:
                    if loc["time"] >= startTime and loc["time"] <= endTime:
                        retLocations.append(loc)

                return jsonify(retLocations), 200

            # else return last location
            return jsonify(locations), 200

        # return error if no device is found
        return jsonify({"error": "No device to get locations from"}), 404

    def delete_locations(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            coll.update_one({"imei": imei}, {"$set": {"locations": []}})
            return jsonify({"message": "locations deleted"}), 200
        return jsonify({"error": "not possible to delete locations"}), 400
