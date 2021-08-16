import datetime
import uuid
from multiprocessing.sharedctypes import Value
from pprint import pprint

import pymongo
from flask import jsonify, request, session
from pymongo.message import update
from werkzeug.exceptions import NotFound

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
    def create_device(
        self,
        name: str,
        imei: str,
        owner: str,
        devicePhoneNumber: str,
        ownerPhoneNumer: str,
    ):
        # Create device Object to write to DB
        coll = db["devices"]
        device = {
            "_id": uuid.uuid4().hex,
            "name": name,
            "imei": imei,
            "owner": owner,
            "devicePhoneNumber": devicePhoneNumber,
            "ownerPhoneNumber": ownerPhoneNumer,
            "battery": 0,
            "locations": [],
        }

        # check if device name is available
        if coll.find_one({"name": device["name"]}):
            return None, ValueError("Device name already exists!")

        # check if device name is available
        if coll.find_one({"devicePhoneNumber": device["devicePhoneNumer"]}):
            return None, ValueError("Device number already exists!")

        # check if device name is available
        if coll.find_one({"imei": device["imei"]}):
            return None, ValueError("Device imei already exists!")

        # Everything okey and new device can be inserted!
        result = coll.insert_one(device)
        if not result.acknowledged:
            return None, ValueError("New Device coulnd't be added to DB")

        return device, None

    # /devices/{imei}
    def get_device_from_db(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            del device["locations"]
            return device, 200
        return jsonify({"error": "No device found"}), 400

    def get_device(self, imei: str):
        coll = db["devices"]

        device = coll.find_one({"imei": imei})

        if device is None:
            return None, ValueError("Couldn't find any Device with the specific imei")

        del device["locations"]

        return device, None

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

    def delete_device(self, user_id: str, imei: str):
        devices_coll = db["devices"]
        user_coll = db["users"]

        # Get and check device
        device = devices_coll.find_one({"imei": imei})
        if device is None:
            return False, ValueError("Couldn't find devices to be deleted.")

        # First try delete deive number in user
        user_filter_rm_imei = {"_id": user_id}, {"$pull": {"devices": device["imei"]}}
        deleted_in_user = user_coll.update_one(user_filter_rm_imei)
        if not deleted_in_user.acknowledged:
            return False, ValueError("Couldn't delete device in User object.")

        # Delete device object now. When not succeeding restore data in user
        deleted = devices_coll.delete_one({"imei": imei})
        if not deleted.acknowledged:
            user_filter_imei = {"_id": user_id}, {"$push": {"devices": device["imei"]}}
            user_coll.update_one(user_filter_imei)
            return False, ValueError("Couldn't delete device. restored data in User")

        return True, None

    def get_device_status(self, imei: str):
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

    def get_device_status_v2(self, imei: str, maxDeltaTime: datetime.timedelta):

        coll = db["devices"]

        # Get device
        device = coll.find_one({"imei": imei})

        # Check device
        if device is None:
            return None, ValueError("Couldn't retrieve device data for status")

        locations = device.get("locations")
        deltaTime = datetime.datetime.now() - locations[len(locations) - 1]["time"]
        if deltaTime > maxDeltaTime:
            # return status active -> is being stolen or moved!
            return "active", None
        else:
            # return status inactive -> tracker is not sending anything the past maxDelta time.
            return "inactive", None

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

    def create_device_location(
        self,
        imei: str,
        time: str,
        latitude: float,
        longitude: float,
        height: float,
        velocity: float,
    ):

        coll = db["devices"]
        location = {}

        # Get/check device
        device = coll.find_one({"imei": imei})
        if device is None:
            return None, ValueError("Couldn't retrieve device data from DB")

        # Check and convert timestring into time.isoformat
        try:
            year = 2000 + int(time[1:3])
            month = int(time[4:6])
            day = int(time[7:9])
            h = int(time[10:12])
            m = int(time[13:15])
            s = int(time[16:18])
            ms = int(time[19:21])
            datetime_object = datetime.datetime(year, month, day, h, m, s, ms)
        except:
            return None, ValueError("Time string couldn't be parsed.")

        # Add all other data
        location["time"] = datetime_object
        location["latitude"] = latitude
        location["longitude"] = longitude
        location["height"] = height
        location["velocity"] = velocity

        # Try update the deivce object with it's new location
        updated = coll.update_one({"imei": imei}, {"$push": {"locations": location}})

        if not updated.acknowledged:
            return None, ValueError("Location couldn't be added to DB")

        # Return updated object
        return location, None

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

    def get_device_locations(self, imei, start_time, end_time):

        computed_start = None
        computed_end = None
        early_date = datetime.datetime(2019, 12, 23)
        now = datetime.datetime.now()

        # Get devices
        coll = db["devices"]

        # Get/check device
        device = coll.find_one({"imei": imei})
        if device is None:
            return None, ValueError("Deivce not found for getting any location(s)")

        # Get/check locations property
        locations = device.get("locations")
        if locations is None or len(locations) == 0:
            return None, ValueError("No locations in device found")

        # Return location if no further computation is needed
        if (start_time is None) and (end_time is None):
            computed_start = early_date
            computed_end = now
        # Compute all locations from start to now
        if (start_time is not None) and (end_time is None):
            computed_start = start_time
            computed_end = now

        # Compute all locations from the first entry to the endTime
        if (start_time is None) and (end_time is not None):
            computed_start = early_date
            computed_end = end_time

        # Compute all locations in the interval [star_time, end_time]
        if (start_time is not None) and (end_time is not None):
            computed_start = start_time
            computed_end = end_time

        # Fill the locations based on the demanded set
        retLocations = []
        for locaction in locations:
            is_location_in_set = (
                locaction["time"] >= computed_start
                and locaction["time"] <= computed_end
            )
            if is_location_in_set:
                retLocations.append(locaction)

        # Check result again
        if locations is None or len(locations) == 0:
            return None, ValueError("No locations in device found for this set")

        # return locations
        return retLocations, None

    def delete_locations(self, imei: str):
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device != None and check_against_userID(device["owner"]):
            coll.update_one({"imei": imei}, {"$set": {"locations": []}})
            return jsonify({"message": "locations deleted"}), 200
        return jsonify({"error": "not possible to delete locations"}), 400

    def delete_locations_v2(self, imei: str):

        # Get/check device
        coll = db["devices"]
        device = coll.find_one({"imei": imei})
        if device is None:
            return False, ValueError("Couldn't retrieve device data from DB")

        # Update and check if it was successful
        updated = coll.update_one({"imei": imei}, {"$set": {"locations": []}})
        if not updated.acknowledged:
            return False, ValueError("Location couldn't be deleted from DB")

        # Return true for successful deletion
        return True, None
