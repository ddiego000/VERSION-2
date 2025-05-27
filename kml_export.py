def export_airspace_to_kml(airspace, filename="airspace.kml"):
    def kml_header():
        return """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Airspace</name>"""

    def kml_footer():
        return "</Document>\n</kml>"

    def navpoint_placemark(point):
        return f"""
    <Placemark>
        <name>{point.name}</name>
        <Point>
            <coordinates>{point.longitude},{point.latitude},0</coordinates>
        </Point>
    </Placemark>"""

    def segment_linestring(origin, dest):
        return f"""
    <Placemark>
        <name>{origin.name} - {dest.name}</name>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>
                {origin.longitude},{origin.latitude},0
                {dest.longitude},{dest.latitude},0
            </coordinates>
        </LineString>
    </Placemark>"""

    def airport_folder(airport):
        placemarks = []

        # SID paths (salidas)
        for sid_num in airport.sids:
            point = airspace.nav_points.get(sid_num)
            if point:
                placemarks.append(f"""
    <Placemark>
        <name>{airport.name} SID: {point.name}</name>
        <Style>
            <IconStyle><color>ff0000ff</color></IconStyle>
        </Style>
        <Point><coordinates>{point.longitude},{point.latitude},0</coordinates></Point>
    </Placemark>""")

        # STAR paths (llegadas)
        for star_num in airport.stars:
            point = airspace.nav_points.get(star_num)
            if point:
                placemarks.append(f"""
    <Placemark>
        <name>{airport.name} STAR: {point.name}</name>
        <Style>
            <IconStyle><color>ff00ff00</color></IconStyle>
        </Style>
        <Point><coordinates>{point.longitude},{point.latitude},0</coordinates></Point>
    </Placemark>""")

        return "\n".join(placemarks)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(kml_header())

        # Write NavPoints
        for point in airspace.nav_points.values():
            f.write(navpoint_placemark(point))

        # Write NavSegments
        for segment in airspace.nav_segments:
            origin = airspace.nav_points.get(segment.origin_number)
            dest = airspace.nav_points.get(segment.destination_number)
            if origin and dest:
                f.write(segment_linestring(origin, dest))

        # Write Airports with SIDs/STARs
        for airport in airspace.nav_airports:
            f.write(airport_folder(airport))

        f.write(kml_footer())
