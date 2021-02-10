import unittest
import graphene
from main import graphqlwfs, Query
from graphene.test import Client
import json

# Need this two lines to read .env
from dotenv import load_dotenv
load_dotenv()

class HelloTestCase(unittest.TestCase):
    def make_request(self, query):
        class Data():
            def decode(self, value):
                return query
        class Request():
            data = Data()
        return Request()

    def test_topographyTopographicArea_blankCall(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { topographyTopographicArea } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['topographyTopographicArea'][0], 'Error: Check your logs')
    
    def test_topographyTopographicArea_comboToidFeatureCodeMake(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { topographyTopographicArea( toid: "osgb1000000000006", featureCode: 10021, make: "Manmade" ) } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['topographyTopographicArea'][0], 'Error: Check your logs')
    
    def test_topographyTopographicArea_lt(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { topographyTopographicArea( first: 5, filter: "{ \\"calculatedAreaValue\\" : {\\"_lt\\" : 60.0 } }" ) } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['topographyTopographicArea'][0], 'Error: Check your logs')
    
    def test_topographyTopographicArea_gt(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { topographyTopographicArea( first: 5, filter: "{ \\"calculatedAreaValue\\" : {\\"_gt\\" : 40.0 } }" ) } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['topographyTopographicArea'][0], 'Error: Check your logs')
    
if __name__ == '__main__':
    unittest.main()
