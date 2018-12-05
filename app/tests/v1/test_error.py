from .basetest import BaseTestCase
from flask import json

class ErrorsTestCase(BaseTestCase):
    def test_page_not_found(self):
        """Tests that an invalid resource request will fail"""
        url = '/adsafdafd'
        result = json.loads(self.get_req(url).data)
        self.assertEqual(result['status'], 404)
