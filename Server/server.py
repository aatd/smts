
from flask import Flask, Response, request
import pymongo
#import json
from bson import json_util

app = Flask(__name__)


# Establish connection to database
try:
    mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=1000)

    db = mongo.smts
    mongo.server_info()

except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")


##############################################
# routes

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "name": request.form["name"],
            "nachname": request.form["nachname"]
        }
        dbResponse = db.users.insert_one(user)

        return Response(
            response=json_util.dumps(
                {"message": "user created", "user_id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        raise


@app.route("/users", methods=["GET"])
def get_user():
    try:
        data = list(db.users.find())

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

##############################################


if __name__ == '__main__':
    app.run(port=8008, debug=True)
