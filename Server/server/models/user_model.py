from flask import request, jsonify, session
from passlib.hash import pbkdf2_sha256
import uuid
import pymongo

############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient(
        "localhost:27017",
        serverSelectionTimeoutMS=1000)

    db = mongo.smts


except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


####################### user class ########################


class User:

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
        
        message = "No one was logged in"
        if 'logged_in' in session:
            message = "logged out "+session["user"]["name"]
        session.clear()
        return jsonify({"message": message}), 200

    def user_update(self):
        coll = db["users"]
        jsonny = request.json

        if session["user"]["_id"] == request.view_args["userID"]:

            # check if password is in request.json -> hash it

            if jsonny.get("password") != -1:
                jsonny["password"] = pbkdf2_sha256.encrypt(jsonny["password"])

            coll.update_one({"_id": session["user"]["_id"]}, {"$set": jsonny})

            updated_user = coll.find_one({"_id": session["user"]["_id"]})
            del updated_user["password"]
            session["user"] = updated_user

            return jsonify(session["user"]), 200

        return jsonify({"error": "could not update user"}), 400

    def delete_user(self):
        coll = db["users"]

        # user can only delete his/her account
        if session["user"]["name"] == request.json["name"]:
            result = coll.delete_one({"name": request.json["name"]})
            if result.acknowledged:
                return jsonify({"message": "user deleted"}), 200

        return jsonify({"message": "could not delete user"}), 400

    def get_user(self):
        coll = db["users"]

        if session["user"]["_id"] == request.view_args["userID"]:
            #user = coll.find_one({"_id":request.view_args["userID"]})
            return jsonify(session["user"]), 200

        return jsonify({"error": "not allowed"}), 400

    def get_devices(self):
        coll = db["devices"]

        #check if user and id in path match
        if session["user"]["_id"] == request.view_args["userID"]:
            device_ids = session["user"]["devices"]
            result = coll.find({"owner":session["user"]["_id"]})
            devices = []
            for el in result:
                devices.append(el)
            return jsonify(devices), 200
        

        return jsonify({"error":"could not get devices"}), 400