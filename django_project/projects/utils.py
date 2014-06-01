import math
from django.contrib.gis.geos import Polygon


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - math.log(
            math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def tile2lon(x, z):
    return x / (2.0 ** z) * 360.0 - 180


def tile2lat(y, z):
    n = math.pi - ((2.0 * math.pi * y) / (2.0 ** z))
    return math.degrees(math.atan(math.sinh(n)))


def polyFromTile(x, y, z):
    north = tile2lat(y, z)
    south = tile2lat(y + 1, z)
    west = tile2lon(x, z)
    east = tile2lon(x + 1, z)
    poly = Polygon((
        (east, north),
        (east, south),
        (west, south),
        (west, north),
        (east, north)
    ))
    return poly
