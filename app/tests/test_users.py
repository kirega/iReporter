import unittest
from app import create_app

app  = create_app()

class FlaskUserTest(unittest.TestCase):
    def test_user_get(self):
        self.app = app.test_client()
        self.app.testing = True
        result = self.app.get('/api/v1/users')
        self.assertEqual(result.status_code, 200)
