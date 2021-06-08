from flask import json, request, jsonify, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid
import pymongo
############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient(
        "localhost:27017",
        serverSelectionTimeoutMS=1000)

    db = mongo.smts
   # mongo.server_info()

except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


####################### user class ########################


class User:
    # id = int
    # name = str
    # password = str
    # phoneNumber = int
    # devices = [int]  # Listenelemente festlegen?

    # def __init__(self, id=0, name="", password="", phoneNumber=0):
    #     self.id = id
    #     self.name = name
    #     self.password = password
    #     self.phoneNumber = phoneNumber
    #     self.devices = []

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def get_user_as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "phoneNumber": self.phoneNumber,
            "devices": self.devices
        }

    def add_user_to_db(self):
        json = request.json
        user = {
            "_id": uuid.uuid4().hex,
            "name": json["name"],
            "password": json["password"],
            "phoneNumber": json["phoneNumber"],
            "devices": []
        }

        # encrypt user password sha256
        user["password"] = pbkdf2_sha256.encrypt(user["password"])
        print(user["_id"])
        try:
            coll = db['users']

            # check if username is available
            if coll.find_one({"name": user["name"]}):
                return jsonify({"error": "User name already taken"}), 400

            coll.insert_one(user)

            return self.start_session(user)

        except Exception as e:
            print("error")
            raise

    def user_login(self):
        coll = db["users"]
        json = request.json
        user = coll.find_one({"name": json["name"]})

        if user and pbkdf2_sha256.verify(json['password'], user['password']):
            return self.start_session(user)

        return jsonify({"error": "wrong username/password"}), 401

    def user_logout(self):
        session.clear()
        return jsonify({"message": "logged out"}), 200

    def delete_user(self):
        coll = db["users"]
        if session["user"]["name"] == request.json["name"]:
            result = coll.delete_one({"name": request.json["name"]})
            if result.acknowledged:
                return jsonify({"message": "user deleted"}), 200

        return jsonify({"message": "could not delete user"}), 400
