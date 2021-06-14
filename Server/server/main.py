
from flask import Flask, request, redirect, session
from functools import wraps

from flask.json import jsonify
from models.user_model import User


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


@app.route("/users/", methods=["POST"])
def create_user():
    return User().add_user_to_db()


@app.route("/users/login/", methods=["GET"])
def user_login():
    return User().user_login()


@app.route("/users/logout/", methods=["GET"])
def user_logout():
    return User().user_logout()


@app.route("/users/<userID>/", methods=["PUT"])
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8008, debug=True)
