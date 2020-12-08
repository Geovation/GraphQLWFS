import unittest
import graphene
from flask import Flask, request
from main import graphqlwfs, Query
from graphene.test import Client

class TestStringMethods(unittest.TestCase):

    def test_hello(self):
  
        schema = graphene.Schema(query=Query)
        client = Client(schema)
        query = ' { hello(count: 5, propertyName: "Type", literal: "Education") } '
        executed = client.execute(query)
        print(executed, flush=True)
        assert executed != {'data': {'hello': 'Error: Check your logs'}}
        
if __name__ == '__main__':
    unittest.main()