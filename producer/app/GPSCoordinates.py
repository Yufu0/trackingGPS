from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import numpy as np


@dataclass
class GPSCoordinates:
    """
        Class GPS Coordinates.
    """
    latitude: float
    longitude: float


    def __str__(self):
        return f"{self.longitude}, {self.latitude}"

    def _getLongitude(self):
        return self.longitude

    def _getLatitude(self):
        return self.latitude

    def _setLongitude(self, longitude: float):
        self.longitude = longitude
        if self.longitude < -180:
            self.longitude += 360
        elif self.longitude > 180:
            self.longitude -= 360
        return self.longitude

    def _setLatitude(self, latitude: float):
        self.latitude = latitude
        if self.latitude < -90:
            self.latitude += 180
        elif self.latitude > 90:
            self.latitude -= 180
        return self.latitude


class GPSTracker:
    """
        Class GPS Tracker.
    """
    def __init__(self, gps_coordinates: Optional[GPSCoordinates]=None):
        if gps_coordinates is None:
            gps_coordinates = GPSCoordinates(43.3189511806897, -0.3603881700351672)

        self.gps_coordinates: GPSCoordinates = gps_coordinates
        self.datetime: Optional[datetime] = datetime.now()

        self.speed: float = np.random.uniform(1e-10, 5e-10)
        self.acceleration: float = 0.0

        self.direction: float = np.random.uniform(0, 2 * np.pi)
        self.angular_speed: float = 0.0

    def __str__(self):
        return f"GPS Tracker: {self.gps_coordinates}"

    def get_gps_coordinates(self):
        return self.gps_coordinates

    def set_gps_coordinates(self, gps_coordinates: GPSCoordinates):
        self.gps_coordinates = gps_coordinates
        return self.gps_coordinates

    def update(self):
        # Update datetime
        now = datetime.now()
        delta = now - self.datetime
        self.datetime = now


        # Update GPS coordinates
        self.gps_coordinates.longitude += self.speed * delta.microseconds * np.cos(self.direction)
        self.gps_coordinates.latitude += self.speed * delta.microseconds * np.sin(self.direction)

        # Update speed and direction
        # self.speed += self.acceleration * delta.microseconds
        self.direction += self.angular_speed * delta.microseconds

        # Update acceleration and angular speed
        # self.acceleration += np.random.normal(0, 0.00001)
        self.angular_speed += np.random.normal(0, 1e-8)
