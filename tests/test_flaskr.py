import unittest
from watershed_api import app

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

    # def test_home_data(self):
    #     # sends HTTP GET request to the application
    #     # on the specified path
    #     result = self.app.get('/?longitude=-72.578659&latitude=46.369599')
    #
    #     # assert the status code of the response
    #     self.assertEqual(result.status_code, 200)

        # assert the response data
        # self.assertEqual(result.data, "Hello World!!!")


if __name__ == '__main__':
    unittest.main()