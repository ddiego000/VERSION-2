from airSpace import AirSpace

def main():
    airspace = AirSpace()
    airspace.load_navpoints("C:/Users/Usuario/Downloads/Cat_nav.txt")
    airspace.load_segments("C:/Users/Usuario/Downloads/Cat_seg.txt")
    airspace.load_airports("C:/Users/Usuario/Downloads/Cat_aer.txt")

    print("🛰️  NavPoints cargados:", len(airspace.nav_points))
    print("🧩  Segments cargados:", len(airspace.nav_segments))
    print("✈️  Airports cargados:", len(airspace.nav_airports))

    print("\nEjemplo NavPoint:")
    print(next(iter(airspace.nav_points.values())))

    print("\nEjemplo NavSegment:")
    print(airspace.nav_segments[0])

    print("\nEjemplo NavAirport:")
    print(next(iter(airspace.nav_airports.values())))
