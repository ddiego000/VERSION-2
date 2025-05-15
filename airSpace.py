from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class AirSpace:
    def __init__(self):
        self.nav_points = {}      # number -> NavPoint
        self.nav_segments = []    # list of NavSegment
        self.nav_airports = []    # list of NavAirport

    def load_navpoints(self, filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue
                try:
                    number = int(parts[0])
                    name = parts[1]
                    lat = float(parts[2])
                    lon = float(parts[3])
                    self.nav_points[number] = NavPoint(number, name, lat, lon)
                except Exception as e:
                    print(f"[ERROR] Line: {line.strip()} -> {e}")

    def load_segments(self, filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                try:
                    origin = int(parts[0])
                    dest = int(parts[1])
                    dist = float(parts[2])
                    self.nav_segments.append(NavSegment(origin, dest, dist))
                except Exception as e:
                    print(f"[ERROR] Segment: {line.strip()} -> {e}")

    def load_airports(self, filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                try:
                    name = parts[0]
                    sid = list(map(int, parts[1].split(","))) if "," in parts[1] else [int(parts[1])]
                    star = list(map(int, parts[2].split(","))) if len(parts) > 2 else []
                    self.nav_airports.append(NavAirport(name, sid, star))
                except Exception as e:
                    print(f"[ERROR] Airport: {line.strip()} -> {e}")

    def load_all(self, path_to_nav_file):
        prefix = path_to_nav_file.replace("_nav.txt", "")
        self.load_navpoints(f"{prefix}_nav.txt")
        self.load_segments(f"{prefix}_seg.txt")
        self.load_airports(f"{prefix}_aer.txt")
