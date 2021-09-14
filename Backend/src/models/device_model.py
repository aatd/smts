import datetime
import uuid
from dateutil import parser
from models.db import db


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
        'Create device Object to write to DB'
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

        # check if device number is available
        if coll.find_one({"devicePhoneNumber": device["devicePhoneNumber"]}):
            return None, ValueError("Device number already exists!")

        # check if device imei is available
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
        'add a location to a device specified by its imei'
        coll = db["devices"]
        location = {}

        # Get/check device
        device = coll.find_one({"imei": imei})
        if device is None:
            return None, ValueError("Couldn't retrieve device data from DB")

        # Set current Battery-Status of Device
        device["battery"] = battery

        # Try Updating device Battery status
        cursor = coll.update_one({"imei": imei}, {"$set": device})
        if not cursor.acknowledged:
            return None, ValueError("Couldn't update Device Battery Status")

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
        'get a device from the database'
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

        device_check = coll.find_one({"imei": imei})

        # Check if device with specified id, belongs to current user
        if not device_check or device_check["owner"] != current_user:
            return None, ValueError("Not allowed")

        # add old locations as dont want to overwrite them
        device["locations"] = device_check["locations"]

        #device["owner"] = current_user
        # Try Updating
        cursor = coll.update_one({"imei": imei}, {"$set": device})

        if not cursor.acknowledged:
            # return None, ValueError("Couldn't update the device object")
            return None, ValueError("DB couldn't update the device object")

        # Get new updated Object
        updated_device = coll.find_one({"imei": device["imei"]})

        if updated_device is None:
            # return None, ValueError("Couldn't get the new device object")
            return None, ValueError("Couldn't get the new device object")

        return updated_device, None

    def delete_device(self, imei: str, user_id: str):
        'delete a device from the database'
        devices_coll = db["devices"]

        # Get and check device
        device = devices_coll.find_one({"imei": imei})

        if device["owner"] != user_id:
            return False, ValueError("Not allowed")

        if device is None:
            return False, ValueError("Couldn't find devices to be deleted.")

        # Delete device object now. When not succeeding restore data in user
        deleted = devices_coll.delete_one({"imei": imei})

        if not deleted.acknowledged:
            return False, ValueError("Couldn't delete device. restored data in User")

        return True, None

    def get_device_status(self, imei: str, maxDeltaTime: datetime.timedelta):
        'returns the status of a device. If locations where added since the maxDeltaTime, status is "active" otherwise "inactive"'

        coll = db["devices"]

        # Get device
        device = coll.find_one({"imei": imei})

        # Check device
        if device is None:
            return None, ValueError("Couldn't retrieve device data for status")

        locations = device.get("locations")
        if len(locations) == 0:
            return "inactive", None

        deltaTime = datetime.datetime.now(
        ) - parser.parse(locations[len(locations) - 1]["time"])
        if deltaTime > maxDeltaTime:
            # return status active -> is being stolen or moved!
            return "active", None
        else:
            # return status inactive -> tracker is not sending anything the past maxDelta time.
            return "inactive", None

    def get_device_locations(self, user_id, imei, start_time: datetime.datetime, end_time: datetime.datetime):
        'returns the locations of a device, if no start and end are given only the last locations is returned. If either start or end or both are given, all locations in between this interval are returned'

        computed_start = None
        computed_end = None
        early_date = datetime.datetime(2019, 12, 23).timestamp() * 1000
        now = datetime.datetime.now().timestamp() * 1000

        # Get devices
        coll = db["devices"]

        # Get/check device
        device = coll.find_one({"imei": imei})

        if device is None:
            return None, ValueError("Device not found for getting any location(s)")
        if device["owner"] != user_id:
            return None, ValueError("Not allowed")

        # Get/check locations property
        locations = device.get("locations")
        if len(locations) == 0:
            return None, ValueError("No locations in device found")

        # Compute all locations from start to now
        if (start_time is not None) and (end_time is None):
            computed_start = start_time.timestamp() * 1000
            computed_end = now

        # Compute all locations from the first entry to the endTime
        if (start_time is None) and (end_time is not None):
            computed_start = early_date
            computed_end = end_time.timestamp() * 1000

        # Compute all locations in the interval [star_time, end_time]
        if (start_time is not None) and (end_time is not None):
            computed_start = start_time.timestamp() * 1000
            computed_end = end_time.timestamp() * 1000

        # Return only last location if no further no timeinterval is given!
        if (start_time is None) and (end_time is None):
            lastloc = locations[-1]
            result = []
            result.append(lastloc)
            return result, None

        # Fill the locations based on the demanded set
        retLocations = []
        for locaction in locations:

            location_date = parser.parse(locaction["time"]).timestamp() * 1000

            is_location_in_set = (
                location_date > computed_start
                and location_date <= computed_end
            )
            if is_location_in_set:
                retLocations.append(locaction)

        # Check result again
        if len(retLocations) == 0:
            return None, ValueError("No locations in device found for this set")

        # return locations
        return retLocations, None

    def delete_locations(self, imei: str, user_id: str):
        'delete locations of a device'

        # Get/check device
        coll = db["devices"]
        device = coll.find_one({"imei": imei})

        if device is None:
            return False, ValueError("Couldn't retrieve device data from DB")

        if device["owner"] != user_id:
            return False, ValueError("Not allowed")

        # Update and check if it was successful
        updated = coll.update_one({"imei": imei}, {"$set": {"locations": []}})
        if not updated.acknowledged:
            return False, ValueError("Location couldn't be deleted from DB")

        # Return true for successful deletion
        return True, None
