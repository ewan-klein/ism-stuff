"""
Queries to extract data from OSM using the Overpass API
"""

import datetime
import overpy
import csv

from shapely.geometry import LineString


api = overpy.Overpass()

def timestamped_csvfile(fn):
    """
    Add timestamp to a filename
    """
    today = "{:%d-%m-%Y}".format(datetime.date.today())
    fn = "{}_{}.csv".format(fn, today)
    return fn


def cats2fields(osmobject, cats):
    row = []
    for cat in cats:
        row.append(osmobject.tags.get(cat))
    try:
        row.append('{}'.format(osmobject.lat))
        row.append('{}'.format(osmobject.lon))
    except AttributeError:
        pass
    return row


def centroid(nodelist):
    """
    Returns a Shapely point
    """
    poly = [(float(node.lat), float(node.lon)) for node in nodelist]

    linestring = LineString(poly)
    return linestring.centroid


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



def shop_nodes(querystring, format='csv', verbose=True):
    """
    Retrieve Edinburgh shops from OSM
    """

    result = api.query(querystring)

    if verbose:
        print("Nodes retrieved: {}".format(len(result.nodes)))
        print("Ways retrieved: {}".format(len(result.ways)))
    if csv:
        rows = [['Name', 'Type', 'Hours', 'Accessible', 'Lat', 'Long']]
        cats = ["name", "shop", "opening_hours", "wheelchair"]
        for node in result.nodes:
            row = cats2fields(node, cats)
            rows.append(row)

        for way in result.ways:
            row = cats2fields(way, cats)
            nodelist = way.nodes
            c = centroid(nodelist)
            row.extend([c.x, c.y])
            rows.append(row)


    if verbose:
        print("Total rows: {}".format(len(rows)))

        return rows
    else:
        for node in result.nodes:
            print("Node: {}".format(node.tags.get("name", "n/a")))
            print("  Shop: {}".format(node.tags.get("shop", "n/a")))
            print("    Lat: {}, Lon: {}".format(node.lat, node.lon))





def bike_paths(querystring, format='csv', verbose=True):
    """
    Retrieve Edinburgh bike paths from OSM
    """
    result = api.query(querystring)






#for way in result.ways:
    #print("Name: %s" % way.tags.get("name", "n/a"))
    #print("  Highway: %s" % way.tags.get("highway", "n/a"))
    #print("  Nodes:")
    #for node in way.nodes:
        #print("    Lat: %f, Lon: %f".format(node.lat, node.lon))


shop_query = """\
    (
    node["shop"](55.867,-3.417,56.021,-2.947);
    way["shop"](55.867,-3.417,56.021,-2.947);
    relation["shop"](55.867,-3.417,56.021,-2.947);
    );
    (._;>;);
    out body;
    """


"""
/*
This shows the cycleway and cycleroute network.
*/

[out:json];

(
  // get cycle route relatoins
  relation[route=bicycle]({{bbox}})->.cr;
  // get cycleways
  way[highway=cycleway]({{bbox}});
  way[highway=path][bicycle=designated]({{bbox}});
);

out body;
>;
out skel qt;

"""

bikepath_query = """\
    (
    relation[route=bicycle](55.867,-3.417,56.021,-2.947);
    way[highway=cycleway](55.867,-3.417,56.021,-2.947);
    way[highway=path][bicycle=designated](55.867,-3.417,56.021,-2.947);
    );
    (._;>;);
    out body;
"""



def extract_shops():
    fn = timestamped_csvfile('edinburgh_shops_from_osm')

    with open(fn, 'w', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerows(shop_nodes(shop_query))
        print("Written rows to {}".format(fn))

if __name__ == "__main__":
    extract_shops()

