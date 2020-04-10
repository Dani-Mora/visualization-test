import json

import geopandas as gpd


def _shp_to_geojson(shp_path: str, geojson_path: str, index: str) -> None:
    """
    Generates geojson file from Shape file

    In order to generate ABS_2018.geojson, we need to:

    1- Download data from http://salutweb.gencat.cat/web/.content/_departament/estadistiques-sanitaries/cartografia/ABS_2018.zip
    2- Unzip into ABS_2018
    3- Call
        _shp_to_geojson(os.path.join('ABS_2018', 'ABS_2018.shp'),
                        'ABS_2018.geojson',
                        index='CODIABS')

    :param shp_path: Shape path. Must be located in the same directory as other
        auxiliar files such as shx.
    :param geojson_path: Destination file
    :param index: Column identifier to use to represent each polygon
    """
    df = gpd.read_file(shp_path)
    # Map to Earth coordinates
    df = df.to_crs(epsg=4326)
    # Make sure id is int-based
    df[index] = df[index].astype(int)
    # Set index
    df = df.set_index(index)
    # Build GeoJSON dictionary
    # Add features manually so field "id" is included
    geo_json = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}
        },
        'features': list(df.iterfeatures())
    }
    with open(geojson_path, 'w') as f:
        json.dump(geo_json, f)


def geojson_data() -> dict:
    with open('ABS_2018.geojson', 'r') as f:
        geo_data = json.loads(f.read())
    return geo_data
