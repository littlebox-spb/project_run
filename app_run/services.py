from datetime import datetime
from haversine import haversine, Unit

class Point:
    def __init__(self, latitude, longitude, time):
        self.latitude = latitude
        self.longitude = longitude
        self.time = time

class DistanceCalculator:
    
    @staticmethod
    def distance(point1, point2):
        if point1.time and point2.time:
            total_seconds = (point2.time-point1.time).total_seconds()
        start_point=(point1.latitude,point1.longitude)
        next_point=(point2.latitude,point2.longitude)
        if start_point and next_point:
            dist=haversine(start_point, next_point, unit=Unit.METERS)
        return {'distance': abs(round(dist,2)), 'speed': abs(round(dist/total_seconds,2))} if total_seconds else {'distance': 0, 'speed': 0}


if __name__ == "__main__":
    p1=Point(57.0,16.0,datetime.strptime("2023-07-20T08:16:30.500000","%Y-%m-%dT%H:%M:%S.%f"))
    p2=Point(77.0,19.0,datetime.strptime("2023-07-20T09:16:30.500000","%Y-%m-%dT%H:%M:%S.%f"))
    print(DistanceCalculator.distance(p1,p2))

