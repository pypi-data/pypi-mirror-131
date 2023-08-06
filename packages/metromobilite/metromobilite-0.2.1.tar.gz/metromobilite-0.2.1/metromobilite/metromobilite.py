import requests
import json
from metromobilite.metromobilite_exception import MetromobiliteRequestException, MetromobiliteInvalidDataException

TIMEOUT = 10

class Metromobilite:
    API_BASE_URL = 'http://data.metromobilite.fr/api/'

    def __init__(self, origin):
        self.origin = origin


    def make_request(self, url, params=None):
        """Make the metromobilite API request"""

        headers = {'origin': self.origin}
        response = requests.get(url, headers=headers, timeout=TIMEOUT, params=params)

        if response.status_code != 200:
            raise MetromobiliteRequestException(response.status_code)

        return self.parse_json(response.content)

    def parse_json(self, content):
        try:
            return json.loads(content)
        except ValueError:
            raise MetromobiliteInvalidDataException()

    def get_stoptimes(self, stop_id):
        url = self.API_BASE_URL + 'routers/default/index/stops/' + stop_id + '/stoptimes'

        return self.make_request(url)

    def get_lines_near(self, x, y, dist=None, details=None):
        url = self.API_BASE_URL + 'linesNear/json'
        params = {'x': x, 'y': y, 'dist': dist, 'details': details}
        return self.make_request(url, params)
