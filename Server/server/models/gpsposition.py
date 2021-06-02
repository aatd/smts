import pymongo
import json
import datetime


############### Establish connection to database ###########
try:
    mongo = pymongo.MongoClient("localhost:27017", serverSelectionTimeoutMS=1000)

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


    ##### Getter and setter
    def latitude(self) -> float:
        """Gets the latitude of this GpsPosition.
        :return: The latitude of this GpsPosition.
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float):
        """Sets the latitude of this GpsPosition.


        :param latitude: The latitude of this GpsPosition.
        :type latitude: float
        """

        self._latitude = latitude

    @property
    def longitude(self) -> float:
        """Gets the longitude of this GpsPosition.


        :return: The longitude of this GpsPosition.
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float):
        """Sets the longitude of this GpsPosition.


        :param longitude: The longitude of this GpsPosition.
        :type longitude: float
        """

        self._longitude = longitude

    @property
    def height(self) -> float:
        """Gets the height of this GpsPosition.


        :return: The height of this GpsPosition.
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height: float):
        """Sets the height of this GpsPosition.


        :param height: The height of this GpsPosition.
        :type height: float
        """

        self._height = height

    @property
    def time(self) -> datetime:
        """Gets the time of this GpsPosition.


        :return: The time of this GpsPosition.
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time: datetime):
        """Sets the time of this GpsPosition.


        :param time: The time of this GpsPosition.
        :type time: datetime
        """

        self._time = time

    @property
    def velocity(self) -> float:
        """Gets the velocity of this GpsPosition.


        :return: The velocity of this GpsPosition.
        :rtype: float
        """
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: float):
        """Sets the velocity of this GpsPosition.


        :param velocity: The velocity of this GpsPosition.
        :type velocity: float
        """

        self._velocity = velocity



    def get_coord_as_dict(self):
        return {
            "lat": self.lat,
            "long": self.lon,
            "speed": self.speed,
            "time": self.time
        }
