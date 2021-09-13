import uuid
from models.db import db

from passlib.hash import pbkdf2_sha256


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
            user["password"] = pbkdf2_sha256.hash(user["password"])
            coll = db["users"]

            # # check if username is available
            # if coll.find_one({"name": user["name"]}):
            #     return None, ValueError("User already exists!")

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

    def user_update(self, userID, json):
        "Updates a user based on his/hers session and rewrites all its property data. Does not change the device information"

        # Get required information
        coll = db["users"]
        user = json
        # delete userid and devicelist from json as they can not be updated here
        #del user["id"]
        #del user["devices"]

        # if user changes password, hash it
        user["password"] = pbkdf2_sha256.hash(user["password"])

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

    def user_get(self, id):
        coll = db["users"]
        user = coll.find_one({"_id": id})

        if user == None:
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
