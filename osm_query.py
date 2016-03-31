"""
Queries to extract data from OSM using the Overpass API
"""

import datetime
import overpy
import csv



api = overpy.Overpass()

def timestamped_csvfile(fn):
    """
    Add timestamp to a filename
    """
    today = "{:%d-%m-%Y}".format(datetime.date.today())
    fn = "{}_{}.csv".format(fn, today)
    return fn


def cats2fields(node, cats):
    row = []
    for cat in cats:
        row.append(node.tags.get(cat))
    row.append('{}'.format(node.lat))
    row.append('{}'.format(node.lon))
    return row


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



def shop_nodes(format='csv', verbose=True):
    """
    Retrieve Edinburgh shops from OSM
    """

    result = api.query("""
    (
    node
        ["shop"]
        (55.867,-3.417,56.021,-2.947);
    );
    (._;>;);
    out body;
    """)

    if verbose:
        print("Nodes retrieved: {}".format(len(result.nodes)))
    if csv:
        rows = [['Name', 'Type', 'Hours', 'Accessible', 'Lat', 'Long']]
        cats = ["name", "shop", "opening_hours", "wheelchair"]
        for node in result.nodes:
            row = cats2fields(node, cats)
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


    fn = timestamped_csvfile('edinburgh_shops_from_osm')

    with open(fn, 'w', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(shop_nodes())
        print("Written rows to {}".format(fn))


