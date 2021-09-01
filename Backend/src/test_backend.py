import json
import unittest
from unittest import TestCase

from main import app


class TestCase(TestCase):

    def setUp(self) -> None:
        self.tester = app.test_client(self)

    def test_index(self):
        
        response = self.tester.get('/v1/',content_type='html/text')
        self.assertEqual(response.status_code,200)
        self.assertTrue(b'alive',response.data)

    def test_login(self):
        
        data = json.dumps(dict(name="niklasnn   ",password="1234Bier"))
        
        response = self.tester.post('/v1/users/login',data=data,content_type='application/json')

        self.assertEqual(response.status_code,200)
    

if __name__ == '__main__':
    unittest.main()