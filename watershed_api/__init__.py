from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import geopandas as gpd

from .api.watershed import WatershedDelimitation
from config import Config

# Load data in memory
gdf = gpd.GeoDataFrame.from_file(Config.GEOJSON_BUCKET)
spatial_index = gdf.sindex


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('latitude', type=float)
    parser.add_argument('longitude', type=float)

    api.add_resource(WatershedDelimitation, '/',
                     resource_class_kwargs={'parser': parser,
                                            'gdf': gdf,
                                            'spatial_index': spatial_index})

    return app
