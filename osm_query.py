import overpy
import csv

api = overpy.Overpass()





def taxi_nodes():
    result = api.query("""
    (
    node
        ["amenity"="taxi"]
        (55.867,-3.417,56.021,-2.947);
    );
    (._;>;);
    out body;
    """)

    for node in result.nodes:
        print("Node: {}".format(node.tags.get("name", "n/a")))
        print("  Amenity: {}".format(node.tags.get("amenity", "n/a")))
        print("    Lat: {}, Lon: {}".format(node.lat, node.lon))



def shop_nodes(format='csv'):

    result = api.query("""
    (
    node
        ["shop"]
        (55.867,-3.417,56.021,-2.947);
    );
    (._;>;);
    out body;
    """)

    if csv:
        rows = [['Name', 'Type', 'Hours', 'Accessible', 'Lat', 'Long']]
        for node in result.nodes:
            row = []
            row.append(node.tags.get("name","N/A"))
            row.append(node.tags.get("shop"))
            row.append(node.tags.get("opening_hours"))
            row.append(node.tags.get("hours"))
            row.append(node.tags.get("wheelchair"))
            row.append('{}'.format(node.lat))
            row.append('{}'.format(node.lon))

            rows.append(row)
        return rows
    else:
        for node in result.nodes:
            print("Node: {}".format(node.tags.get("name", "n/a")))
            print("  Shop: {}".format(node.tags.get("shop", "n/a")))
            print("    Lat: {}, Lon: {}".format(node.lat, node.lon))


#result = api.query("""
#way(55.867,-3.417,56.021,-2.947)["highway"];
#(._;>;);
#out body;
#""")


#for way in result.ways:
    #print("Name: %s" % way.tags.get("name", "n/a"))
    #print("  Highway: %s" % way.tags.get("highway", "n/a"))
    #print("  Nodes:")
    #for node in way.nodes:
        #print("    Lat: %f, Lon: %f".format(node.lat, node.lon))

if __name__ == "__main__":

    with open('shops.csv', 'w', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(shop_nodes())


