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
