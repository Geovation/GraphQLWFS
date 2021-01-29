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
    def test_topographyTopographicArea_one_feature(self, mocked_get):
        response_data = {"features": ["I'm getting this"]}
        query = ' { topographyTopographicArea(first: 1) } '
        expected_value = {'topographyTopographicArea': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    @patch('main.requests.get')
    def test_topographyTopographicArea_two_features(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2"]}
        query = ' { topographyTopographicArea(first: 2) } '

        expected_value = {'topographyTopographicArea': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)
    
    @patch('main.requests.get')
    def test_topographyTopographicArea_empty_filter_parameters(self, mocked_get):
        response_data = {"features": ["I'm getting this 1", "I'm getting this 2"]}
        query = ' { topographyTopographicArea(first: 2, theme: "", descriptiveGroup: " ") } '

        expected_value = {'topographyTopographicArea': response_data["features"]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    @patch('main.requests.get')
    def test_topographyTopographicArea_counter_negative(self, mocked_get):
        response_data = 'Error: First needs to be 0 or more'
        query = ' { topographyTopographicArea(first: -5) } '

        expected_value = {'topographyTopographicArea': [response_data]}
        mocked_get.return_value = self.make_mocked_response(response_data)
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(result, expected_value)

    def test_topographyTopographicArea_buildWFSQuery_single_filter(self):
        first = 1
        typeNames = "osfeatures:Topography_TopographicArea"
        filters = {
            "TOID": "osgb1000000000006",
            "featureCode": None,
            "theme": None,
            "calculatedAreaValue": None,
            "reasonForChange": None,
            "descriptiveGroup": None,
            "make": None,
            "physicalLevel": None
        }
        payload = buildWFSQuery(first, typeNames, filters)

        self.assertEqual(payload['count'], first)
        self.assertEqual(payload['typeNames'], typeNames)

        stripedPayloadFilter = payload['filter'].replace(
            ' ', '').replace('\n', '')
        expectedFilter = """<Filter>
                                <PropertyIsEqualTo>
                                    <PropertyName>TOID</PropertyName>
                                    <Literal>osgb1000000000006</Literal>
                                    </PropertyIsEqualTo>
                            </Filter>"""
        stripedExpectedFilter = expectedFilter.replace(' ', '').replace('\n', '')

        self.assertEqual(stripedPayloadFilter, stripedExpectedFilter)

    def test_topographyTopographicArea_buildWFSQuery_triple_filter(self):
        first = 1
        typeNames = "osfeatures:Topography_TopographicArea"
        filters = {
            "TOID": "osgb1000000000006",
            "featureCode": 10021,
            "theme": None,
            "calculatedAreaValue": None,
            "reasonForChange": None,
            "descriptiveGroup": None,
            "make": "Manmade",
            "physicalLevel": None
        }
        payload = buildWFSQuery(first, typeNames, filters)

        self.assertEqual(payload['count'], first)
        self.assertEqual(payload['typeNames'], typeNames)

        stripedPayloadFilter = payload['filter'].replace(
            ' ', '').replace('\n', '')
        expectedFilter = """<Filter>
                                <And>
                                    <PropertyIsEqualTo>
                                        <PropertyName>TOID</PropertyName>
                                        <Literal>osgb1000000000006</Literal>
                                    </PropertyIsEqualTo>
                                    <PropertyIsEqualTo>
                                        <PropertyName>featureCode</PropertyName>
                                        <Literal>10021</Literal>
                                    </PropertyIsEqualTo>
                                    <PropertyIsEqualTo>
                                        <PropertyName>make</PropertyName>
                                        <Literal>Manmade</Literal>
                                    </PropertyIsEqualTo>
                                </And>
                            </Filter>"""
        stripedExpectedFilter = expectedFilter.replace(' ', '').replace('\n', '')

        self.assertEqual(stripedPayloadFilter, stripedExpectedFilter)


if __name__ == '__main__':
    unittest.main()
