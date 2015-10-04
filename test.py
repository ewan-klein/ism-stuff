import overpy
api = overpy.Overpass()

result = api.query("""
way(55.867,-3.417,56.021,-2.947)["highway"];
(._;>;);
out body;
""")

for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print("  Highway: %s" % way.tags.get("highway", "n/a"))
    print("  Nodes:")
    for node in way.nodes:
        print("    Lat: %f, Lon: %f".format(node.lat, node.lon))