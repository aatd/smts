from datetime import timedelta
from functools import wraps

from flask import Flask, request, session
from flask.json import jsonify
from flask_cors import CORS
from werkzeug.wrappers import accept

from models.device_model import Device
<<<<<<< HEAD
from flask_cors import CORS
=======
from models.user_model import User

version = "v1"
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8

app = Flask(__name__)
app.secret_key = "myThiefBackendSecretKey123"
CORS(app)
<<<<<<< HEAD
version = "/v1"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
=======
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8

# Decorators
# function that wraps routes that require login otherwise redirect to home


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=12)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "not allowed, log in first"})

    return wrap


##############################################
# routes

<<<<<<< HEAD
#go away from my home
@app.route(f"{version}/",methods=["GET"])
=======
# go away from my home
@app.route(f"/{version}/", methods=["GET"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
def go_home():
    return "go home", 200


# Users
<<<<<<< HEAD
@app.route(f"{version}/users", methods=["POST"])
=======
@app.route(f"/{version}/users", methods=["POST"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
def create_user():
    return User().add_user_to_db()


<<<<<<< HEAD
@app.route(f"{version}/users/login", methods=["GET"])
=======
@app.route(f"/{version}/users/login", methods=["POST"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
def user_login():
    return User().user_login()


<<<<<<< HEAD
@app.route(f"{version}/users/logout", methods=["GET"])
=======
@app.route(f"/{version}/users/logout", methods=["GET"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
def user_logout():
    return User().user_logout()


<<<<<<< HEAD
@app.route(f"{version}/users/<userID>", methods=["PUT"])
=======
@app.route(f"/{version}/users/<userID>", methods=["PUT"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def update_user(userID):
    return User().user_update()

<<<<<<< HEAD
@app.route(f"{version}/users/<userID>", methods=["GET"])
=======

@app.route(f"/{version}/users/<userID>", methods=["GET"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def get_user(userID):
    return User().get_user()


<<<<<<< HEAD
@app.route(f"{version}/users/<userID>", methods=["DELETE"])
=======
@app.route(f"/{version}/users/<userID>", methods=["DELETE"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def delete_user():
    return User().delete_user()


<<<<<<< HEAD
@app.route(f"{version}/users/<userID>/devices", methods=["GET"])
=======
@app.route(f"/{version}/users/<userID>/devices", methods=["GET"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def get_devices_from_user(userID):
    return User().get_devices()


<<<<<<< HEAD
@ app.route(f"{version}/input", methods=["GET"])
=======
@app.route(f"/{version}/input", methods=["GET"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
def input_from_device():
    return server.input_from_device(request)


##############################################
# devices

<<<<<<< HEAD
@app.route(f"{version}/devices", methods=["POST"])
=======

@app.route(f"/{version}/devices", methods=["POST"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def create_device():
    return Device().add_device_to_db()

<<<<<<< HEAD
@app.route(f"{version}/devices/<imei>", methods= ["GET"])
=======

@app.route(f"/{version}/devices/<imei>", methods=["GET"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
def get_device(imei):
    return Device().get_device_from_db(imei)


<<<<<<< HEAD
@app.route(f"{version}/devices/<imei>", methods=["DELETE"])
=======
@app.route(f"/{version}/devices/<imei>", methods=["DELETE"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def delete_device(imei):
    return Device().delete_device_from_db(imei)


<<<<<<< HEAD
@app.route(f"{version}/devices/<imei>/locations", methods =["GET"])
=======
@app.route(f"/{version}/devices/<imei>/locations", methods=["GET"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def get_locations(imei):
    return Device().get_locations_from_db(imei)

<<<<<<< HEAD
@app.route(f"{version}/devices/<imei>/locations", methods =["POST"])
=======

@app.route(f"/{version}/devices/<imei>/locations", methods=["POST"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
def add_locations(imei):
    return Device().add_position_to_device(imei)


<<<<<<< HEAD

@app.route(f"{version}/devices/<imei>/locations", methods = ["DELETE"])
=======
@app.route(f"/{version}/devices/<imei>/locations", methods=["DELETE"])
>>>>>>> ca6bb43ff79398a7b36b135f6ade2eaac89d1af8
@login_required
def delete_locations(imei):
    return Device().delete_locations(imei)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
