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
            "devices": []
        }
        return userd


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


###################### device class #######################
class device:
    id = ""
    coords = []

    def add_coordinate(self, coordinate):
        self.coords.append(coordinate)
