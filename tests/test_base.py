import unittest
from watershed_api import app
import numpy as np
import geopandas as gpd

app.testing = True


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client = app
        self.client.testing = True

    def tearDown(self):
        pass

    # def create_app(self):
    #     app = Flask(__name__)
    #     # app.config['TESTING'] = True
    #     return app

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        with self.client.test_client() as client:
            result = client.get('/',
                                data={'longitude': -72.578659,
                                      'latitude': 46.369599}
                                )
            self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # sends HTTP GET request to the application
        # on the specified path

        result = np.ceil(
            gpd.GeoDataFrame \
            .from_features(self.client.get('/',
                                           data={'longitude': -72.578659,
                                                 'latitude': 46.369599}) \
                           .json(), crs=4326) \
            .to_crs(epsg=32198).area.values[0] / 1000000)

        # assert  of the response
        self.assertEqual(result, 41774.0)



if __name__ == '__main__':
    unittest.main()
