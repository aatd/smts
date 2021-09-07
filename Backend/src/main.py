import datetime
from datetime import timedelta
from functools import wraps

from flask import Flask, request, session
from flask.json import jsonify
from flask_cors import CORS

from models.device_model import Device
from models.user_model import User

app = Flask(__name__)
app.secret_key = "myThiefBackendSecretKey123"
app.config[
    "SESSION_COOKIE_HTTPONLY"
] = False  # So the cookie is readable in browser. UNSAFE!
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
    app.permanent_session_lifetime = timedelta(minutes=30)


##############################################
# Routes


@app.route(f"{version}/", methods=["GET"])
def is_server_alive():
    "Returns a HTTP 200 to indicate that the server is online"

    # Just return a 200. Later maybe some status, and health information.
    return "server is alive", 200


# Users routes


@app.route(f"{version}/users", methods=["POST"])
def create_user():
    "Creates a new User Object. Returns 201 when successfull. Returns 409 when creating with wrong parameters!"

    # Get required data
    json = request.json
    name = json.get("name")
    pwd = json.get("password")
    tel = json.get("phoneNumber")

    # Check if all data are aquired
    if None in (name, pwd, tel):
        return "There is some information missing!", 409

    # Check if username already taken
    tmp_user = User().user_get_data(name)
    if tmp_user is not None:
        return "Username already taken!", 409

    # Attemp user creation
    userData, err = User().create_user(name, pwd, tel)

    # Create valid session
    start_session(userData)

    # Error check
    if (err is not None) or (userData is None):
        return "DB error", 409

    return userData, 201


@app.route(f"{version}/users/login", methods=["POST"])
def login_user():
    "Attempts a login by check the required parameter. When successeded returning HTTP 200, the session-cookie and the corresponing user object. If not succesful it return HTTP 401"

    # Get required data
    json = request.json
    name = json.get("name")
    pwd = json.get("password")

    # Check if authorized
    if not User().user_auth(name, pwd):
        return "Login Failed", 401

    # Get userdata
    userData = User().user_get_data(request.json["name"])
    if userData is None:
        return "Login Failed", 401

    # Everything went well.
    # Start session by setting the sesssion-cookie
    start_session(userData)

    # Return data
    return userData, 200


@app.route(f"{version}/users/logout", methods=["POST"])
@login_required
def logout_user():
    "Apptemps a Logut by clearing the session-cookie. HTTP 200 when successful, else 401."

    # You have a valid sesion. So we ca nnow log you out
    stop_session()

    # Return data
    return "Logged out successfully", 200


@app.route(f"{version}/users/<userID>", methods=["PUT"])
@login_required
def update_user(userID):
    "Updates a user object. HTTP 204 if successeded. When failed return HTTP 400"

    # Get required data
    json = request.json
    session_user_id = session["user"]["_id"]
    name = json["name"]
    pwd = json["password"]
    if userID != session_user_id:

        return "Not allowed", 405

    updated_user, err = User().user_update(userID, json)

    # Error check
    if (updated_user is None) or (err is not None):
        return str(err), 400

    # Return
    return jsonify(updated_user), 201


@app.route(f"{version}/users/<userID>", methods=["GET"])
@login_required
def get_user(userID):
    "Return the User Object based on the requested session. Return 404 else."

    # Get required data
    session_user_id = session["user"]["_id"]

    # Try get user from DB if requested user is logged in
    if session_user_id != userID:
        return "Not allowed", 405

    userData, err = User().user_get(userID)

    # Error check
    if (err is not None) or (userData is None):
        return "Couldn't get Userdata", 404

    # return data
    return userData, 200


@app.route(f"{version}/users/<userID>", methods=["DELETE"])
@login_required
def delete_user(userID):
    "Delete a speciif user based on a current valid session. Return"

    # Get data from session
    username = session["user"]["name"]
    session_userID = session["user"]["_id"]

    # Check if user is permitted
    if session_userID != userID:
        return "Not allowed", 405

    # Try deleting from Database
    deleted, err = User().user_delete(username, userID)
    if (deleted is not True) or (err is not None):
        return "Couldn't delete User.", 401

    # Return ok
    session.clear()
    return "User deleted", 200


@app.route(f"{version}/users/<userID>/devices", methods=["GET"])
@login_required
def get_user_devices(userID):

    # Get required data from request
    user_id = session["user"]["_id"]

    # Try get all data from DB
    devices, error = User().user_get_devices(user_id)

    # Error check
    if (devices is None) or (error is not None):
        return "No devices found", 404

    # Return data
    return jsonify(devices), 200


##############################################
# devices


@app.route(f"{version}/devices", methods=["POST"])
@login_required
def create_device():
    "Creates a new Device Object. Returns 201 when successfull. Returns 409 when creating with wrong parameters!"

    # Get required data
    json = request.json
    name = json.get("name")
    imei = json.get("imei")
    tel = json.get("devicePhoneNumber")
    pin = json.get("pin")
    apn = json.get("apn")
    apnUser = json.get("apnUser")
    apnPassword = json.get("apnPassword")
    owner = session["user"]["_id"]
    ownerTel = session["user"]["phoneNumber"]

    # Check if all data are aquired
    if None in (name, imei, tel, pin, apn, apnUser, apnPassword, owner):
        return "There is some information missing!", 409

    # Attemp user creation
    deviceData, err = Device().create_device(
        name, imei, owner, tel, ownerTel, apn, apnUser, apnPassword, pin
    )

    # Error check
    if (err is not None) or (deviceData is None):
        return str(err), 409

    return deviceData, 201


@app.route(f"{version}/devices/<imei>", methods=["GET"])
@login_required
def get_device(imei):
    "Return the User Object based on the requested session. Return 404 else."

    # Try get user from DB
    deviceData, err = Device().get_device(imei)

    # Error check
    if (err is not None) or (deviceData is None):
        return "Couldn't get Userdata", 404

    if session["user"]["_id"] != deviceData["owner"]:
        return "Not allowed", 405

    # return data
    return deviceData, 200


@app.route(f"{version}/devices/<imei>", methods=["PUT"])
@login_required
def update_device(imei):
    "Updates the device, if the imei belongs to the current user"

    # get the session id to check if device belongs to current user
    session_id = session["user"]["_id"]
    # The changes are stored in the json data of the request
    json = request.json

    # Try updating the device by passing the new settings
    updated_device, err = Device().device_update(json, session_id, imei)

    if (err is not None) or (update_device is None):
        if "Not allowed" in str(err):
            return str(err), 405
        return str(err), 404

    # return updated device
    return updated_device, 200


@app.route(f"{version}/devices/<imei>", methods=["DELETE"])
@login_required
def delete_device(imei):

    user_id = session["user"]["_id"]
    # Try deletion
    deleted, error = Device().delete_device(imei, user_id)

    # Check wethe deletion was successful
    if (deleted is not True) or (error is not None):

        if "Not allowed" in str(error):
            return str(error), 405

        return str(error), 400

    # Return data
    return "Device deleted successfully", 200


@app.route(f"{version}/devices/<imei>/status", methods=["GET"])
@login_required
def get_device_status(imei):

    # Compute maximum time we define the bike as active
    maxDelta = datetime.timedelta(minutes=60)

    # Try getting the current status
    status, error = Device().get_device_status(imei, maxDelta)

    # Check wether there is an error with the output
    if (error is not None) or (status is None):
        return "Status cannot be found", 404

    # return data
    return jsonify(status), 200


@app.route(f"{version}/devices/<imei>/locations", methods=["GET"])
@login_required
def get_locations(imei):

    # Get datetime minima/maxima
    try:
        start_value = float(request.args.get("start"))
        start_time = datetime.datetime.fromtimestamp(start_value//1000)
    except:
        start_time = None
    try:
        end_value = float(request.args.get("end"))
        end_time = datetime.datetime.fromtimestamp(end_value//1000)
    except:
        end_time = None

    # Get userid from session
    user_id = session["user"]["_id"]

    # Attempt get data from database
    locations, error = Device().get_device_locations(
        user_id, imei, start_time, end_time)

    # Check for error
    if (error is not None) or (len(locations) == 0):
        if "Not allowed" in str(error):
            return str(error), 405
        return str(error), 204
    # Return data
    return jsonify(locations), 200


@app.route(f"{version}/devices/<imei>/locations", methods=["POST"])
def create_locations(imei):

    # Get required data from request
    json = request.json
    lat = json.get("latitude")
    lng = json.get("longitude")
    time = json.get("time")
    vel = json.get("velocity")
    bat = json.get("battery")

    # Check if all data are aquired
    if None in (lat, imei, lng, time):
        return "There are some informations missing!", 409

    # Try create new Locations on device
    new_location, error = Device().create_device_location(
        imei, time, lat, lng, vel, bat
    )

    if (new_location is None) or (error is not None):
        return str(error), 409

    return new_location, 201


@app.route(f"{version}/devices/<imei>/locations", methods=["DELETE"])
@login_required
def delete_locations(imei):

    user_id = session["user"]["_id"]
    # Attempt deletion
    deleted, error = Device().delete_locations(imei, user_id)

    # Check wethe deletion was successful
    if not deleted or error is not None:
        if "Not allowed" in str(error):
            return str(error), 405
        return str(error), 400

    # Return data
    return "All device locations deleted successfully", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
