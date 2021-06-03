import json
from typing import List

import pymongo
from bson import ObjectId, json_util
from flask import Flask, Response, request
from geojson import Point

from gpsposition import gpsPosition

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

    def get_device_as_dict(self):
        return {
            ""
            "imei": self.imei,
            "coords": self.coords
        }

    def add_coordinate(self, coordinate):
        self.coords.append(coordinate)
        try:
            myquery = {"imei": self.imei}
            newvalues = {
                "$push": {
                    "coords": json_util.dumps(
                        coordinate.get_coord_as_dict())}}
            result = db.devices.update_one(myquery, newvalues)
            return result.acknowledged

        except Exception as e:
            raise

