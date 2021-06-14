from gpsposition_model import GpsPosition
from datetime import date, datetime
import json
from typing import List
import pprint
import pymongo
from bson import ObjectId, json_util
from flask import Flask, Response, request
from geojson import Point


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
    locations: List[GpsPosition]

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
            "ownerPhoneNumber": self.ownerPhoneNumber,
            "locations": locs
        }

    def add_location(self, location):
        self.locations.append(location)


def get_devices_by_user() -> List[Device]:
    pass


def get_device_from_db(imei: int) -> Device:
    pass


def add_device_to_db(device: Device) -> Device:

    try:
        coll = db['devices']
        dict_device = device.as_dict()
        result = coll.insert_one(dict_device)

        if(result.acknowledged):
            new_dev = coll.find_one({"_id": result.inserted_id})
            return new_dev

    except Exception as e:
        print("error")
        raise


def add_position_to_device(dev: Device, position: GpsPosition) -> bool:
    pass


def get_locations_from_db(dev: Device) -> List[GpsPosition]:
    pass


def delete_device_from_db(dev: Device) -> bool:
    pass
