from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import numpy as np


@dataclass
class GPSCoordinates:
    """
        Class GPS Coordinates.
    """
    longitude: float
    latitude: float

    def __str__(self):
        return f"{self.longitude}, {self.latitude}"


class GPSTracker:
    """
        Class GPS Tracker.
    """
    def __init__(self, gps_coordinates: Optional[GPSCoordinates]=None):
        if gps_coordinates is None:
            gps_coordinates = GPSCoordinates(0.0, 0.0)
        self.gps_coordinates: GPSCoordinates = gps_coordinates
        self.datetime: Optional[datetime] = datetime.now()

        self.speed: float = 1.0
        self.acceleration: float = 0.0

        self.direction: float = 0.0
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
        self.gps_coordinates.longitude += self.speed * delta.seconds * np.cos(self.direction)
        self.gps_coordinates.latitude += self.speed * delta.seconds * np.sin(self.direction)

        # Update speed and direction
        self.speed += self.acceleration * delta.seconds
        self.direction += self.angular_speed * delta.seconds

        # Update acceleration and angular speed
        self.acceleration += np.random.normal(0, 0.001)
        self.angular_speed += np.random.normal(0, 0.001)
