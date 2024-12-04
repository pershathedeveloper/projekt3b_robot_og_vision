class Path:
    def __init__(self, waypoints=None):
        self.waypoints = waypoints if waypoints else []

    def addWaypoint(self, position):
        self.waypoints.append(position)
