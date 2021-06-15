from flask import Flask, request, session
from functools import wraps

from flask.json import jsonify
from models.user_model import User
from models.device_model import Device


app = Flask(__name__)
app.secret_key = "myThiefBackendSecretKey123"

# Decorators
# function that wraps routes that require login otherwise redirect to home


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "not allowed, log in first"})

    return wrap


##############################################
# routes

# Users
@app.route("/users/", methods=["POST"])
def create_user():
    return User().add_user_to_db()




@app.route("/users/login/", methods=["GET"])
def user_login():
    return User().user_login()


@app.route("/users/logout/", methods=["GET"])
def user_logout():
    return User().user_logout()


@app.route("/users/<userID>", methods=["PUT"])
@login_required
def update_user(userID):
    return User().user_update()

@app.route("/users/<userID>/", methods=["GET"])
@login_required
def get_user(userID):
    return User().get_user()


@app.route("/users/<userID>/", methods=["DELETE"])
@login_required
def delete_user():
    return User().delete_user()


@app.route("/users/<userID>/devices/", methods=["GET"])
@login_required
def get_devices_from_user(userID):
    return User().get_devices()


@ app.route("/input/", methods=["GET"])
def input_from_device():
    return server.input_from_device(request)

##############################################
# devices

@app.route("/devices/", methods=["POST"])
@login_required
def create_device():
    return Device().add_device_to_db()

@app.route("/devices/<imei>", methods= ["GET"])
def get_device(imei):
    return Device().get_device_from_db(imei) 

@app.route("/devices/<imei>", methods=["DELETE"])
@login_required
def delete_device(imei):
    return Device().delete_device_from_db(imei)  

@app.route("/devices/<imei>/locations", methods =["GET"])
@login_required
def get_locations(imei):
    return Device().get_locations_from_db(imei)

@app.route("/devices/<imei>/locations", methods =["POST"])
@login_required
def add_locations(imei):
    return Device().add_position_to_device(imei)

@app.route("/devices/<imei>/locations", methods = ["DELETE"])
@login_required
def delete_locations(imei):
    return Device().delete_locations(imei)    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8008, debug=False)
