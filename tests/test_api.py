import unittest
import json
from app import create_app, db
from app.models import Machine, Cluster, Tag


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.client.get(
            '/api/url')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['error'], 'not found')
