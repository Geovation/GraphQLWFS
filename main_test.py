import unittest
import graphene
from six import assertCountEqual
from main import graphqlwfs, Query
from graphene.test import Client
from unittest.mock import Mock, patch

class HelloTestCase(unittest.TestCase):
    # def make_mocked_request_get(data):
    #     def mocked_request_get(*args, **kwargs):
    #         class mockResponse:
    #             status_code = 200
    #             def json(_): return data
    #         return mockResponse()
    #     return mocked_request_get

    def make_mocked_response(self,data):
        class mockResponse:
            status_code = 200
            def json(_): return data
        return mockResponse()

    def make_request(self, query):
        class Data():
            def decode(self, value):
                return query
        class Request():
            data = Data()
        return Request()

    # @patch('main.requests.get', new=make_mocked_request_get('my query here'))
    @patch('main.requests.get')
    def test_single_feature(self, mocked_get):
        response_data = {"features": ["I'm getting this"]}
        query = ' { hello(count: 2, propertyName: "Type", literal: "Education") } '
        expected_value = {'hello': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)


    @patch('main.requests.get')
    def test_two_features(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2"]}
        query = ' { hello(count: 2, propertyName: "Type", literal: "Education") } '

        expected_value = {'hello': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)


if __name__ == '__main__':
    unittest.main()
