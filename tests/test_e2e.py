import unittest
import graphene
from main import graphqlwfs, Query
from graphene.test import Client

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

    def test_zoomstackSites_no_errors(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { zoomstackSites(count: 5, propertyName: "Type", literal: "Education") } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['zoomstackSites'][0], 'Error: Check your logs')

    def test_zoomstackSites_count_1_feature(self):
        query = ' { zoomstackSites(count: 1, propertyName: "Type", literal: "Education") } '
        request = self.make_request(query)
        result = graphqlwfs(request)
        
        self.assertEqual(len(result["zoomstackSites"]), 1)

    def test_zoomstackSites_count_2_features(self):
        query = ' { zoomstackSites(count: 2, propertyName: "Type", literal: "Education") } '
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(len(result["zoomstackSites"]), 2)
    
    def test_zoomstackSites_negative_count(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { zoomstackSites(count: -1, propertyName: "Type", literal: "Education") } '
        executed = client.execute(query)

        self.assertEqual(executed['data']['zoomstackSites'][0],'Error: Count needs to be 0 or more')

    def test_zoomstackSites_empty_filter(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { zoomstackSites(count: 2, propertyName: " " , literal: "    ") } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['zoomstackSites'][0], 'Error: Check your logs')
    
    def test_zoomstackNames_no_errors(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { zoomstackNames(count: 5, propertyName: "Type", literal: "National Park") } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['zoomstackNames'][0], 'Error: Check your logs')

    def test_zoomstackNames_count_1_feature(self):
        query = ' { zoomstackNames(count: 1, propertyName: "Type", literal: "National Park") } '
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(len(result["zoomstackNames"]), 1)

    def test_zoomstackNames_count_2_features(self):
        query = ' { zoomstackNames(count: 2, propertyName: "Type", literal: "National Park") } '
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(len(result["zoomstackNames"]), 2)
    
    def test_zoomstackNames_negative_count(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { zoomstackNames(count: -2, propertyName: "Type", literal: "National Park") } '
        executed = client.execute(query)

        self.assertEqual(executed['data']['zoomstackNames'][0],'Error: Count needs to be 0 or more')

    def test_zoomstackNames_empty_filter(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { zoomstackNames(count: 5, propertyName: "", literal: "  ") } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['zoomstackNames'][0], 'Error: Check your logs')

    def test_zoomstackNames_name1(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { zoomstackNames(count: 5, propertyName: "Type", literal: "City", name1: "Aberdeen") } '
        executed = client.execute(query)

        self.assertNotEqual(executed['data']['zoomstackNames'][0], 'Error: Check your logs')

if __name__ == '__main__':
    unittest.main()
