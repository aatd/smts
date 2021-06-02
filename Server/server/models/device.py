from geojson import Point
from flask import Flask, Response, request
import pymongo
import json
from bson import ObjectId, json_util


############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient("localhost:27017", serverSelectionTimeoutMS=1000)

    db = mongo.smts
   # mongo.server_info()

except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


class device:
    imei = ""
    coords = []

    def get_device_as_dict(self):
        return {

            "imei": self.imei,
            "coords": self.coords
        }

    def add_coordinate(self, coordinate):
        self.coords.append(coordinate)
        try:
            myquery = {"imei": self.imei}
            newvalues = {"$push": {"coords": json_util.dumps(coordinate.get_coord_as_dict())}}
            result = db.devices.update_one(myquery, newvalues)
            return result.acknowledged

        except Exception as e:
            raise
