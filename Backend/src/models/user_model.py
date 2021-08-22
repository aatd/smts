from socket import socket
import uuid
import os

import pymongo
from passlib.hash import pbkdf2_sha256

##############################################
# Init DB
try:

    print("Trying to connect to User-DB located at: " +
          os.environ["DATABASE_IP"])
    mongo = pymongo.MongoClient(os.environ["DATABASE_IP"], 27017)
    db = mongo.smts
    print(
        "Trying to connect to DB located at: "
        + os.environ["DATABASE_IP"]
        + "...Successful"
    )

except pymongo.errors.ConnectionFailure as err:
    print(
        "Trying to connect to User-DB located at: "
        + os.environ["DATABASE_IP"]
        + "...Failed...Err: "
        + err
    )
    exit(1)


class User:

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
            coll.insert(user)

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
