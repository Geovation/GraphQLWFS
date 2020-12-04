import unittest
import graphene
from flask import Flask, request
from main import graphqlwfs

class TestStringMethods(unittest.TestCase):

    def test_hello(self):
        self.assertIsNotNone(graphqlwfs('{hello(count:5, propertyName: "Type", literal: "Education")}'))

  

if __name__ == '__main__':
    unittest.main()