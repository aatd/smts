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

    # /users
    def add_user_to_db(self):
        if "logged_in" not in session:

            try:
                json = request.json
                user = {
                    "_id": uuid.uuid4().hex,
                    "name": json["name"],
                    "password": json["password"],
                    "phoneNumber": json["phoneNumber"],
                    "devices": [],
                }

            except:
                print("requestData invalid")
                return jsonify({"error": "requestData invalid"}), 409

            try:
                # encrypt user password sha256
                user["password"] = pbkdf2_sha256.encrypt(user["password"])
                coll = db["users"]

                # check if username is available
                if coll.find_one({"name": user["name"]}):
                    return jsonify({"error": "User name already taken"}), 409

                coll.insert_one(user)

                return self.start_session(user, session)

            except:
                print("DB error")
                return jsonify({"error": "requestData invalid"}), 409
        else:
            return jsonify({"error": "log out first"})

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

    # /users/login
    def user_login(self):
        coll = db["users"]
        if not "logged_in" in session:

            json = request.json
            user = coll.find_one({"name": json["name"]})

            if user and pbkdf2_sha256.verify(json["password"], user["password"]):
                return self.start_session(user, session)

            return jsonify({"error": "wrong username/password"}), 401

        return jsonify({"message": "log out first"}), 409

    # /users/login
    def user_auth(self):
        coll = db["users"]

        json = request.json
        user = coll.find_one({"name": json["name"]})

        if user and pbkdf2_sha256.verify(json["password"], user["password"]):
            return True

        return False

    # /users/logout
    def user_logout(self):
        message = "No one was logged in"
        if "logged_in" in session:
            message = "logged out"
        session.clear()
        return jsonify({"message": message}), 200

    # /users/{userId}
    def user_update(self):
        coll = db["users"]
        jsonObject = request.json

        if jsonObject.get("password") != None:
            jsonObject["password"] = pbkdf2_sha256.encrypt(jsonObject["password"])

        coll.update_one({"_id": session["user"]["_id"]}, {"$set": jsonObject})

        updated_user = coll.find_one({"_id": session["user"]["_id"]})
        del updated_user["password"]
        session["user"] = updated_user

        return jsonify(session["user"]), 200

    # /users/{userId}
    def user_update_v2(self, userID, name=None, password=None, phonenumber=None):
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

        return jsonify(updated_user), None

    # /users/{userId}
    def delete_user(self):
        coll = db["users"]

        # user can only delete his/her account
        if session["user"]["name"] == request.json["name"]:
            result = coll.delete_one({"name": request.json["name"]})
            if result.acknowledged:
                session.clear()
                return jsonify({"message": "user deleted"}), 200

        return jsonify({"message": "could not delete user"}), 400

        # /users/{userId}

    def delete_user_v2(self, username, id):
        "Triy to delete User"

        # Get all Users
        coll = db["users"]

        # Acutally try to delete here by checking if name and id are correct
        result = coll.delete_one({"name": username, "_id": id})
        if not result.acknowledged:
            return False, ValueError("Couldn't delete User")

        # Everything went well
        return True, None

    def get_user(self):
        coll = db["users"]

        if session["user"]["_id"] == request.view_args["userID"]:
            # user = coll.find_one({"_id":request.view_args["userID"]})
            return jsonify(session["user"]), 200

        return jsonify({"error": "not allowed"}), 400

    def user_get(self, id, username):
        coll = db["users"]
        user = coll.find_one({"_id": id})

        if user["name"] != username:
            return None, ValueError("DB Error: Couldn't find entry")

        return user, None

    def get_userdata(self, name):
        coll = db["users"]
        return coll.find_one({"name": name})

    def get_devices(self):
        coll = db["devices"]

        result = coll.find({"owner": session["user"]["_id"]})

        devices = []
        for device in result:
            del (
                device["locations"],
                device["_id"],
                device["owner"],
                device["ownerPhoneNumber"],
            )
            devices.append(device)
        jsonObject = jsonify(devices)
        return jsonObject, 200

    def get_user_devices(self):
        "Get the Users Devices from DB"

        # Try get DB-Entries based on the UserID
        coll = db["devices"]
        result = coll.find({"owner": session["user"]["_id"]})
        if result is None:
            return None, ValueError("No device/s found.")

        # Make List of all Devices
        devices = []
        for device in result:
            del (
                device["locations"],
                device["_id"],
                device["owner"],
                device["ownerPhoneNumber"],
            )
            devices.append(device)
        jsonObject = jsonify(devices)
        return jsonObject, 200
