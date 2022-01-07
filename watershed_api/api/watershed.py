from shapely.geometry import Point
from flask_restful import Resource


class WatershedDelimitation(Resource):

    def __init__(self,
                 parser,
                 gdf,
                 spatial_index):
        """

        Parameters
        ----------
        parser
        gdf
        spatial_index
        """
        self.parser = parser
        self.gdf = gdf
        self.spatial_index = spatial_index

    def get(self):
        """

        Returns
        -------
        (geo-)Json string

        """
        args = self.parser.parse_args()
        latitude = args['latitude']
        longitude = args['longitude']
        coordinates = (longitude, latitude)

        gdf_basin = self._watershed_from_coordinates(coordinates)

        return gdf_basin.__geo_interface__

    def _watershed_from_coordinates(self,
                                    coordinates,
                                    ):
        """

        Parameters
        ----------
        coordinates

        Returns
        -------

        """

        gdf = self.gdf
        spatial_index = self.spatial_index

        point = Point(coordinates)

        # find index of sub-basin (polygon) on which the selected coordinate/point falls on
        possible_matches = gdf.iloc[list(spatial_index.intersection(point.bounds))]
        polygon_index = possible_matches[possible_matches.intersects(point)]

        # find all sub-basins indexes upstream of polygon_index
        gdf_main_basin = gdf[gdf['MAIN_BAS'].isin(polygon_index['MAIN_BAS'])]
        all_sub_basins_indexes = self._recursive_upstream_lookup(gdf_main_basin,
                                                                 polygon_index['HYBAS_ID'].to_list())
        all_sub_basins_indexes.extend(polygon_index['HYBAS_ID'])

        # create GeoDataFrame from all sub-basins indexes and dissolve to a unique basin (new unique index)
        gdf_sub_basins = gdf_main_basin[gdf_main_basin['HYBAS_ID'].isin(set(all_sub_basins_indexes))]
        gdf_basin = gdf_sub_basins.dissolve(by='MAIN_BAS')

        # keep largest polygon if multi polygon
        if gdf_basin.iloc[0].geometry.geom_type == 'MultiPolygon':
            gdf_basin.loc[gdf_basin.index, 'geometry'] = max(gdf_basin.iloc[0].geometry,
                                                             key=lambda a: a.area)
        return gdf_basin

    def _recursive_upstream_lookup(self,
                                   gdf,
                                   direct_upstream_indexes,
                                   all_upstream_indexes=None):
        """

        Parameters
        ----------
        gdf
        direct_upstream_indexes
        all_upstream_indexes

        Returns
        -------

        """
        if all_upstream_indexes is None:
            all_upstream_indexes = []

        # get direct upstream indexes
        direct_upstream_indexes = gdf[gdf['NEXT_DOWN'].isin(direct_upstream_indexes)]['HYBAS_ID'].to_list()
        if len(direct_upstream_indexes) > 0:
            all_upstream_indexes.extend(direct_upstream_indexes)
            self._recursive_upstream_lookup(gdf, direct_upstream_indexes, all_upstream_indexes)
        return all_upstream_indexes
