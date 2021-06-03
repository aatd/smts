import datetime
import json


class gpsPosition:

    latitude: float
    longitude: float
    height: float
    time: datetime.datetime
    velocity: float

    def __init__(self, latitude=0.0, longitude=0.0,
                 height=0.0, time=datetime.datetime(1, 1, 1, 1, 1, 1), velocity=0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.time = time
        self.velocity = velocity

    def as_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "height": self.height,
            "time": self.time.strftime("%m/%d/%Y %H:%M:%S"),
            "velocity": self.velocity
        }
