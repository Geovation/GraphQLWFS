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

    def test_no_errors(self):
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { hello(count: 5, propertyName: "Type", literal: "Education") } '
        executed = client.execute(query)
        assert executed != {'data': {'hello': 'Error: Check your logs'}}

    def test_resutn_1_feature(self):
        query = ' { hello(count: 1, propertyName: "Type", literal: "Education") } '
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(len(result["hello"]), 1)

    def test_resutn_2_features(self):
        query = ' { hello(count: 2, propertyName: "Type", literal: "Education") } '
        request = self.make_request(query)
        result = graphqlwfs(request)

        self.assertEqual(len(result["hello"]), 2)
if __name__ == '__main__':
    unittest.main()
