from datetime import timedelta
from functools import wraps

from flask import Flask, request, session
from flask_cors import CORS
from pymongo.common import _UUID_REPRESENTATIONS

from models.device_model import Device
from models.user_model import User

app = Flask(__name__)
app.secret_key = "myThiefBackendSecretKey123"
app.config["SESSION_COOKIE_HTTPONLY"] = False  # So the cookie is readable in browser.
CORS(app, supports_credentials=True)
version = "/v1"

##############################################
# Middleware
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return "Login first", 401

    return wrap


##############################################
# Session
def start_session(user):
    del user["password"]
    session["logged_in"] = True
    session["user"] = user


def stop_session():
    session.clear()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=12)


##############################################
# Routes


@app.route(f"{version}/", methods=["GET"])
def is_server_alive():
    "Returns a HTTP 200 to indicate that the server is online"
    return "server is alive", 200


# Users
@app.route(f"{version}/users", methods=["POST"])
def create_user():
    "Creates a new User Object. Returns 201 when succefull. Returns 409 when having gived the wrong parameters!"

    json = request.json
    name = json.get("name")
    pwd = json.get("password")
    tel = json.get("phoneNumber")

    if None in (name, pwd, tel):
        return "There are some information missing!", 409

    userData, err = User().create_user(name, pwd, tel)

    if err is not None:
        return "DB error", 409

    return userData, 201


@app.route(f"{version}/users/login", methods=["POST"])
def login_user():
    if User().user_auth():
        userData = User().get_userdata(request.json["name"])
        start_session(userData)
        return userData, 201
    else:
        return "Login Failed", 401


@app.route(f"{version}/users/logout", methods=["POST"])
def logout_user():
    if "logged_in" in session:
        stop_session()
        return "Logged out successfully", 200
    else:
        return "Logout Failed", 401


@app.route(f"{version}/users/<userID>", methods=["PUT"])
@login_required
def update_user(userID):
    return User().user_update()


@app.route(f"{version}/users/<userID>", methods=["GET"])
@login_required
def get_user(userID):
    "Return the User Object based on the requested session. Return 404 else."
    session_id = session["user"]["_id"]
    userData, err = User().user_get(session_id, userID)

    if err is not None:
        return "Couldn't get Userdata", 404

    return userData, 200


@app.route(f"{version}/users/<userID>", methods=["DELETE"])
@login_required
def delete_user():
    "Delete a speciif user based on a current valid session. Return"

    # Get data from session
    username = session["user"]["name"]
    userID = session["user"]["_id"]

    # Try deleting from Database
    deleted, err = User().delete_user_v2(username, userID)
    if not deleted | err is not None:
        return "Couldn't delete User.", 401

    # Return ok
    return "User deleted", 200


@app.route(f"{version}/users/<userID>/devices", methods=["GET"])
@login_required
def get_devices_from_user(userID):
    return User().get_devices()


@app.route(f"{version}/input", methods=["GET"])
def input_from_device():
    return server.input_from_device(request)


##############################################
# devices


@app.route(f"{version}/devices", methods=["POST"])
@login_required
def create_device():
    return Device().add_device_to_db()


@app.route(f"{version}/devices/<imei>", methods=["GET"])
@login_required
def get_device(imei):
    return Device().get_device_from_db(imei)


@app.route(f"{version}/devices/<imei>", methods=["DELETE"])
@login_required
def delete_device(imei):
    return Device().delete_device_from_db(imei)


@app.route(f"{version}/devices/<imei>/status", methods=["GET"])
def get_device_status(imei):
    return Device().get_device_status(imei)


@app.route(f"{version}/devices/<imei>/locations", methods=["GET"])
@login_required
def get_locations(imei):
    return Device().get_locations_from_db(imei)


@app.route(f"{version}/devices/<imei>/locations", methods=["POST"])
def add_locations(imei):
    return Device().add_position_to_device(imei)


@app.route(f"{version}/devices/<imei>/locations", methods=["DELETE"])
@login_required
def delete_locations(imei):
    return Device().delete_locations(imei)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
