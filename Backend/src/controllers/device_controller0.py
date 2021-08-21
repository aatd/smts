from geojson import Point
from flask import Flask, Response, request
import pymongo
import json
from bson import ObjectId, json_util
import models


def get_user(username):
    return models.get_user_by_name(username)


def create_user_server(request):
    name = request.form["name"]
    surname = request.form["surname"]
    return models.create_user_models(name, surname)


def input_from_device(request):
    imei = request.args["id"]
    device = models.device()
    if len(models.get_device_by_imei(imei).imei) < 1:
        device = models.add_device_to_db(imei)

    else:
        device = models.get_device_by_imei(imei)

    coord = models.coordinate()

    coord.lat = request.args["latitude"]
    coord.lon = request.args["longitude"]
    coord.speed = request.args["speed"]

    if device.add_coordinate(coord):
        return Response(
            response=str(models.get_device_by_imei(imei).coords),
            status=200,
            mimetype="text/html"
        )
    else:
        return Response(
            response=str("cannot add coordinate"),
            status=500,
            mimetype="text/html"
        )
