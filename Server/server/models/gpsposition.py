import datetime
import json

import pymongo

############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient(
        "localhost:27017",
        serverSelectionTimeoutMS=1000)

    db = mongo.smts
   # mongo.server_info()

except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")

####################### coordinate class ########################


class gpsPosition:
    latitude: float
    longitude: float
    height: float
    time: datetime.datetime
    velocity: float

    def get_coord_as_dict(self):
        return {
            "lat": self.lat,
            "long": self.lon,
            "speed": self.speed,
            "time": self.time
        }
