import unittest
from main import graphqlwfs, fetchFeaturesFromWFS, buildWFSQuery
from unittest.mock import patch

class HelloTestCase(unittest.TestCase):
    # def make_mocked_request_get(data):
    #     def mocked_request_get(*args, **kwargs):
    #         class mockResponse:
    #             status_code = 200
    #             def json(_): return data
    #         return mockResponse()
    #     return mocked_request_get

    
    # testing main
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
    
    @patch('main.requests.get')
    def test_empty_filter_parameters(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2", "I'm getting this also"]}
        query = ' { hello(count: 2, propertyName: "", literal: " ") } '

        expected_value = {'hello': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    @patch('main.requests.get')
    def test_counter_negative(self, mocked_get):
        response_data = 'Error: Count needs to be 0 or more'
        query = ' { hello(count: -5, propertyName: "Type", literal: "Education") } '

        expected_value = {'hello': [response_data]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    def test_buildWFSQuery_hello(self):
        count = 1
        typeNames = None
        filters = {
            "Type": "Education"
        }
        payload = buildWFSQuery(count, typeNames, filters)

        self.assertEqual(payload['count'], count)
        self.assertEqual(payload['typeNames'], typeNames)

        stripedPayloadFilter = payload['filter'].replace(
            ' ', '').replace('\n', '')
        expectedFilter = """<Filter>
                                <PropertyIsEqualTo>
                                    <PropertyName>Type</PropertyName>
                                    <Literal>Education</Literal>
                                    </PropertyIsEqualTo>
                            </Filter>"""
        stripedExpectedFilter = expectedFilter.replace(' ', '').replace('\n', '')

        self.assertEqual(stripedPayloadFilter, stripedExpectedFilter)


if __name__ == '__main__':
    unittest.main()
