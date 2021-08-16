import uuid
from os import error

import pymongo
from flask import jsonify, request, session
from passlib.hash import pbkdf2_sha256

##############################################
# Init DB
try:
    mongo = pymongo.MongoClient("localhost:27017", serverSelectionTimeoutMS=1000)
    db = mongo.smts
except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


class User:
    def start_session(self, user):
        del user["password"]
        session["logged_in"] = True
        session["user"] = user
        return jsonify(user), 201

    def create_user(self, name, pwd, tel):

        # Check and prepare DB-Entry
        try:
            # Create User Object to write to DB
            user = {
                "_id": uuid.uuid4().hex,
                "name": name,
                "password": pwd,
                "phoneNumber": tel,
                "devices": [],
            }

            # encrypt user password sha256
            user["password"] = pbkdf2_sha256.encrypt(user["password"])
            coll = db["users"]

            # check if username is available
            if coll.find_one({"name": user["name"]}):
                return None, ValueError("User already exists!")

            # Everything okey and new User can be inserted!
            coll.insert_one(user)

            return user, None

        except ValueError as err:
            return None, err

    def user_auth(self, username, password):
        coll = db["users"]

        user = coll.find_one({"name": username})

        if user and pbkdf2_sha256.verify(password, user["password"]):
            return True

        return False

    def user_update(self, userID, name=None, password=None, phonenumber=None):
        "Updates a user based on his/hers session and rewrites all its property data. Does not change the device information"

        # Get required information
        coll = db["users"]
        user = {}

        # Try checking each property
        if name is not None:
            user["name"] = name

        if password is not None:
            user["password"] = pbkdf2_sha256.encrypt(password)

        if phonenumber is not None:
            user["phoneNumber"] = phonenumber

        # Sanity check of properties
        if (
            coll.find_one({"name": user["name"]})
            and coll.find_one({"_id": userID})["name"] != user["name"]
        ):  # Does User already exists?
            return None, ValueError("User already exisits")

        # Try Updating
        cursor = coll.update_one({"_id": userID}, {"$set": user})
        if not cursor.acknowledged:
            return None, ValueError("Couldn't rewrite the UserObject")

        # Get new updated Object
        updated_user = coll.find_one({"_id": userID})
        if updated_user is None:
            return None, ValueError("Couldn't get the new UserObject")

        # Password hash is not required
        del updated_user["password"]

        return updated_user, None

    def user_delete(self, username, id):
        "Triy to delete User"

        # Get all Users
        coll = db["users"]

        # Acutally try to delete here by checking if name and id are correct
        result = coll.delete_one({"name": username, "_id": id})
        if not result.acknowledged:
            return False, ValueError("Couldn't delete User")

        # Everything went well
        return True, None

    def user_get(self, id, username):
        coll = db["users"]
        user = coll.find_one({"_id": id})

        if user["name"] != username:
            return None, ValueError("DB Error: Couldn't find entry")

        del user["password"]

        return user, None

    def user_get_data(self, name):
        coll = db["users"]
        return coll.find_one({"name": name})

    def user_get_devices(self, id):
        coll = db["devices"]

        result = coll.find({"owner": id})
        if result is None:
            return None, ValueError("No devices found")

        devices = []
        for device in result:
            del (
                device["locations"],
                device["_id"],
                device["owner"],
                device["ownerPhoneNumber"],
            )
            devices.append(device)

        return devices, None
