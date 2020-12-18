import unittest
from main import graphqlwfs, get_feature, build_query
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
            def json(self): return data
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
    def test_zoomstackSites_one_feature(self, mocked_get):
        response_data = {"features": ["I'm getting this"]}
        query = ' { zoomstackSites(count: 2, propertyName: "Type", literal: "Education") } '
        expected_value = {'zoomstackSites': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    @patch('main.requests.get')
    def test_zoomstackSites_two_features(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2"]}
        query = ' { zoomstackSites(count: 2, propertyName: "Type", literal: "Education") } '

        expected_value = {'zoomstackSites': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)
    
    @patch('main.requests.get')
    def test_zoomstackSites_empty_filter_parameters(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2", "I'm getting this also"]}
        query = ' { zoomstackSites(count: 2, propertyName: "", literal: " ") } '

        expected_value = {'zoomstackSites': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    @patch('main.requests.get')
    def test_zoomstackSites_counter_negative(self, mocked_get):
        response_data = 'Error: Count needs to be 0 or more'
        query = ' { zoomstackSites(count: -5, propertyName: "Type", literal: "Education") } '

        expected_value = {'zoomstackSites': [response_data]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    def test_zoomstackSites_build_query(self):
        count = 1
        typeNames = "Zoomstack_Sites"
        filters = {
            "Type": "Education"
        }
        payload = build_query(count, typeNames, filters)

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

    @patch('main.requests.get')
    def test_zoomstackNames_one_feature(self, mocked_get):
        response_data = {"features": ["I'm getting this"]}
        query = ' { zoomstackNames(count: 2, propertyName: "Type", literal: "National Park") } '
        expected_value = {'zoomstackNames': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    @patch('main.requests.get')
    def test_zoomstackNames_two_features(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2"]}
        query = ' { zoomstackNames(count: 2, propertyName: "Type", literal: "National Park") } '

        expected_value = {'zoomstackNames': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)
    
    @patch('main.requests.get')
    def test_zoomstackNames_empty_filter_parameters(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2", "I'm getting this also"]}
        query = ' { zoomstackNames(count: 2, propertyName: "", literal: " ") } '

        expected_value = {'zoomstackNames': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    @patch('main.requests.get')
    def test_zoomstackNames_counter_negative(self, mocked_get):
        response_data = 'Error: Count needs to be 0 or more'
        query = ' { zoomstackNames(count: -5, propertyName: "Type", literal: "National Park") } '

        expected_value = {'zoomstackNames': [response_data]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    def test_zoomstackNames_build_query(self):
        count = 1
        typeNames = "Zoomstack_Names"
        filters = {
            "propertyName": "Type",
            "literal": "City",
            "name1": ""
        }

        payload = build_query(count, typeNames, filters)

        self.assertEqual(payload['count'], count)
        self.assertEqual(payload['typeNames'], typeNames)

        stripedPayloadFilter = payload['filter'].replace(
            ' ', '').replace('\n', '')
        expectedFilter = """<Filter>
                                <PropertyIsEqualTo>
                                    <PropertyName>Type</PropertyName>
                                    <Literal>City</Literal>
                                </PropertyIsEqualTo>
                            </Filter>"""
        stripedExpectedFilter = expectedFilter.replace(' ', '').replace('\n', '')

        self.assertEqual(stripedPayloadFilter, stripedExpectedFilter)

    def test_zoomstackNames_build_query_name1(self):
        count = 1
        typeNames = "Zoomstack_Names"
        filters = {
            "propertyName": "Type",
            "literal": "City",
            "name1": "Aberdeen"
        }

        payload = build_query(count, typeNames, filters)

        self.assertEqual(payload['count'], count)
        self.assertEqual(payload['typeNames'], typeNames)

        stripedPayloadFilter = payload['filter'].replace(
            ' ', '').replace('\n', '')
        expectedFilter = """<Filter>
                                <And>
                                    <PropertyIsEqualTo>
                                        <PropertyName>Type</PropertyName>
                                        <Literal>City</Literal>
                                    </PropertyIsEqualTo>
                                    <PropertyIsEqualTo>
                                        <PropertyName>Name1</PropertyName>
                                        <Literal>Aberdeen</Literal>
                                    </PropertyIsEqualTo>
                                </And>
                            </Filter>"""
        stripedExpectedFilter = expectedFilter.replace(' ', '').replace('\n', '')

        self.assertEqual(stripedPayloadFilter, stripedExpectedFilter)


if __name__ == '__main__':
    unittest.main()
