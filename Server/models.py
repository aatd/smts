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


####################### user class ########################
class user:
    id = ""
    name = ""
    surname = ""
    devices = []

    def get_user_as_dict(self):
        userd = {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "devices": self.devices
        }
        return userd

####################### device class ########################
###################### device class #######################


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


def add_device_to_db(imei):
    try:
        tmpDevice = device()
        tmpDevice.imei = imei
        db.devices.insert_one(tmpDevice.get_device_as_dict())

    except Exception as e:
        raise

    return tmpDevice


def get_device_by_imei(imei):
    try:
        data = list(db.devices.find({"imei": imei}))
        tmpDevice = device()
        if(len(data) > 0):

            tmpDevice.id = data[0]["_id"]
            tmpDevice.imei = data[0]["imei"]
            tmpDevice.coords = data[0]["coords"]
            return tmpDevice
    except Exception as e:
        raise

    return tmpDevice

####################### coordinate class ########################


class coordinate:
    lat = ""
    lon = ""
    speed = ""
    time = ""

    def get_coord_as_dict(self):
        return {
            "lat": self.lat,
            "long": self.lon,
            "speed": self.speed,
            "time": self.time
        }


def create_user_models(name, surname):
    try:
        tmpUser = user()
        tmpUser.name = name
        tmpUser.surname = surname
        tmpUser.id = db.users.insert_one(tmpUser.get_user_as_dict()).inserted_id
        return Response(
            response=json_util.dumps(ObjectId(tmpUser.id)),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        raise


def get_user_by_name(username):
    try:
        data = list(db.users.find({"name": username}))

        return Response(
            response=json_util.dumps(data),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        print(e)
        return Response(
            response=json_util.dumps(
                {"message": "cannot read user"}),
            status=500,
            mimetype="application/json"
        )
