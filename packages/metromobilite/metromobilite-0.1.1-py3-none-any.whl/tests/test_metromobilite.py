import pytest
import requests_mock
from metromobilite import Metromobilite
from metromobilite.metromobilite_exception import MetromobiliteInvalidDataException, MetromobiliteRequestException



class TestMetromobilite:
    def setup_class(self):
        self.m = Metromobilite(origin='Test request')

    def test_make_request_exception(self):
        with requests_mock.Mocker() as r:
            r.get("https://example.com", status_code=404)
            with pytest.raises(MetromobiliteRequestException):
                self.m.make_request("https://example.com")
    
    def test_parse_json(self):
        json = """{"test": "test"}"""
        content = self.m.parse_json(json)
        assert {'test': 'test'} == content


    def test_parse_json_exception(self):
        with pytest.raises(MetromobiliteInvalidDataException):
            self.m.parse_json("")

    def test_get_stoptimes(self):
         with requests_mock.Mocker() as r:
            stop_id = "test"
            r.get(self.m.API_BASE_URL + 'routers/default/index/stops/' + stop_id + '/stoptimes' , json="""{"test": "test"}""")
            response = self.m.get_stoptimes(stop_id)
            assert """{"test": "test"}""" == response
