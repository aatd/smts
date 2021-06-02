from flask import Flask, request
import models
import server

app = Flask(__name__)


##############################################
# routes
@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    return server.get_user(username)


@app.route("/users", methods=["POST"])
def create_user_run():
    return server.create_user_server(request)


@app.route("/input", methods=["GET"])
def input_from_device():
    return server.input_from_device(request)

##############################################


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8008, debug=True)
