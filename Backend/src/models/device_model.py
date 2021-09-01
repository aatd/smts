import datetime
import os
import uuid
from dateutil import parser


import pymongo

##############################################
# Init DB
try:

    if os.environ.get("DATABASE_IP") is not None:
        db_location = os.environ["DATABASE_IP"] + ":27017"
    else:
        db_location = "localhost:27017"

    print("Trying to connect to Device-DB located at: " + db_location)
    # mongo = pymongo.MongoClient(os.environ["DATABASE_IP"], 27017)
    mongo = pymongo.MongoClient(db_location, serverSelectionTimeoutMS=1000)
    db = mongo.smts
    print("Trying to connect to DB located at: " + db_location + "...Successful")
    print(db.last_status)

except pymongo.errors.ConnectionFailure as err:

    if os.environ.get("DATABASE_IP") is not None:
        db_location = os.environ["DATABASE_IP"] + ":27017"
    else:
        db_location = "localhost:2017"

    print(
        "Trying to connect to Device-DB located at: "
        + db_location
        + "...Failed...Err: "
        + err
    )
    exit(1)


class Device:
    def create_device(
        self,
        name: str,
        imei: str,
        owner: str,
        devicePhoneNumber: str,
        ownerPhoneNumer: str,
        apn: str,
        apnUser: str,
        apnPassword: str,
        pin: str,
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
            "apn": apn,
            "apnUser": apnUser,
            "apnPassword": apnPassword,
            "pin": pin,
            "locations": [],
        }

        # check if device name is available
        if coll.find_one({"name": device["name"]}):
            return None, ValueError("Device name already exists!")

        # check if device name is available
        if coll.find_one({"devicePhoneNumber": device["devicePhoneNumber"]}):
            return None, ValueError("Device number already exists!")

        # check if device name is available
        if coll.find_one({"imei": device["imei"]}):
            return None, ValueError("Device imei already exists!")

        # Everything okey and new device can be inserted!
        result = coll.insert_one(device)
        if not result.acknowledged:
            return None, ValueError("New Device coulnd't be added to DB")

        return device, None

    def create_device_location(
        self,
        imei: str,
        time: str,
        latitude: float,
        longitude: float,
        velocity: float,
        battery: float,
    ):

        coll = db["devices"]
        location = {}

        # Get/check device
        device = coll.find_one({"imei": imei})
        if device is None:
            return None, ValueError("Couldn't retrieve device data from DB")

        # Add all other data
        location["time"] = time
        location["latitude"] = latitude
        location["longitude"] = longitude
        location["battery"] = battery
        location["velocity"] = velocity

        # Try update the deivce object with it's new location
        updated = coll.update_one(
            {"imei": imei}, {"$push": {"locations": location}})

        if not updated.acknowledged:
            return None, ValueError("Location couldn't be added to DB")

        # Return updated object
        return location, None

    def get_device(self, imei: str):
        coll = db["devices"]

        device = coll.find_one({"imei": imei})

        if device is None:
            return None, ValueError("Couldn't find any Device with the specific imei")

        del device["locations"]

        return device, None

    def device_update(self, json, current_user, imei):
        "updates a device with the given data, only if device owner and current session user are the same"

        # Get required information
        coll = db["devices"]
        device = json

        # remove locations and battery, they should not be changed here
        del device["locations"]
        del device["battery"]

        x = coll.find_one({"imei": imei})

        # Check if device with specified id, belongs to current user
        if not x or x["owner"] != current_user:
            return ValueError("Device not updateable")
            # return None, ValueError("Device not updateable")

        device["owner"] = current_user
        # Try Updating
        cursor = coll.update_one({"imei": device["imei"]}, {"$set": device})
        if not cursor.acknowledged:
            # return None, ValueError("Couldn't update the device object")
            return ValueError("Couldn't update the device object")

        # Get new updated Object
        updated_device = coll.find_one({"imei": device["imei"]})
        if updated_device is None:
            # return None, ValueError("Couldn't get the new device object")
            return ValueError("Couldn't get the new device object")

        return updated_device

    def delete_device(self, imei: str):
        devices_coll = db["devices"]

        # Get and check device
        device = devices_coll.find_one({"imei": imei})
        if device is None:
            return False, ValueError("Couldn't find devices to be deleted.")

        # Delete device object now. When not succeeding restore data in user
        deleted = devices_coll.delete_one({"imei": imei})
        if not deleted.acknowledged:
            return False, ValueError("Couldn't delete device. restored data in User")

        return True, None

    def get_device_status(self, imei: str, maxDeltaTime: datetime.timedelta):

        coll = db["devices"]

        # Get device
        device = coll.find_one({"imei": imei})

        # Check device
        if device is None:
            return None, ValueError("Couldn't retrieve device data for status")

        locations = device.get("locations")
        deltaTime = datetime.datetime.now(
        ) - locations[len(locations) - 1]["time"]
        if deltaTime > maxDeltaTime:
            # return status active -> is being stolen or moved!
            return "active", None
        else:
            # return status inactive -> tracker is not sending anything the past maxDelta time.
            return "inactive", None

    def get_device_locations(self, imei, start_time: datetime.datetime, end_time: datetime.datetime):

        computed_start = None
        computed_end = None
        early_date = datetime.datetime(2019, 12, 23).timestamp() * 1000
        now = datetime.datetime.now().timestamp() * 1000

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

        # Compute all locations from start to now
        if (start_time is not None) and (end_time is None):
            computed_start = start_time.timestamp() * 1000
            computed_end = end_time.timstamp() * 1000

        # Compute all locations from the first entry to the endTime
        if (start_time is None) and (end_time is not None):
            computed_start = early_date
            computed_end = end_time.timestamp() * 1000

        # Compute all locations in the interval [star_time, end_time]
        if (start_time is not None) and (end_time is not None):
            computed_start = start_time.timestamp() * 1000
            computed_end = end_time

            # Return location if no further computation is needed
        if (start_time is None) and (end_time is None):
            computed_start = early_date
            computed_end = now

        # Fill the locations based on the demanded set
        retLocations = []
        for locaction in locations:

            location_date = parser.parse(locaction["time"]).timestamp() * 1000

            is_location_in_set = (
                location_date >= computed_start
                and location_date <= computed_end
            )
            if is_location_in_set:
                retLocations.append(locaction)

        # Check result again
        if locations is None or len(locations) == 0:
            return None, ValueError("No locations in device found for this set")

        # return locations
        return retLocations, None

    def delete_locations(self, imei: str):

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
