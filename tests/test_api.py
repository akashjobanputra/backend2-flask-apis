import unittest
import json
from app import create_app, db
from app.models import Machine, Cluster, Tag, MachineState

machines = [
    {
        "name": "DEV_CACHE_OPTIMIZER",
        "ip_address": "ABCD:ABCD:CE3A:ABCD:CCCC:ABCD",
        "instance_type": "medium",
        "tags": ["DEV", "IND", "CACHE"]
    },
    {
        "name": "DEV_NOTIFICATIONS",
        "ip_address": "ABCD:ABCD:CE3A:ABCD:CCCC:73AB",
        "instance_type": "small",
        "tags": ["DEV", "IND"]
    }
]

cluster = {
    "name": "DevIN", "cloud_region": "IND_MUM"
}


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

    def test_clusters(self):
        response = self.client.get('/api/clusters')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['clusters']), 0)

        response = self.client.post('/api/clusters',
                                    data=json.dumps(cluster),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['id'], 1)
        self.assertEqual(len(response.get_json()['machines']), 0)

        # add machines to cluster
        response = self.client.post("/api/clusters/1/machines",
                                    data=json.dumps(machines[0]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['id'], 1)
        self.assertEqual(len(response.get_json()['tags']), 3)

        response = self.client.post("/api/clusters/1/machines",
                                    data=json.dumps(machines[1]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['id'], 2)
        self.assertEqual(len(response.get_json()['tags']), 2)

        response = self.client.get('/api/clusters/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['cluster']['machines']), 2)

        # Check tags in machine
        response = self.client.get('/api/clusters/1/machines')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['machines'][0]['tags']), 3)
        self.assertIn('dev', response.get_json()['machines'][0]['tags'])

    def test_machine_operations(self):
        # Adding Data
        response = self.client.post('/api/clusters',
                                    data=json.dumps(cluster),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['id'], 1)
        self.assertEqual(len(response.get_json()['machines']), 0)

        # add machines to cluster
        response = self.client.post("/api/clusters/1/machines",
                                    data=json.dumps(machines[0]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['id'], 1)
        self.assertEqual(len(response.get_json()['tags']), 3)

        response = self.client.post("/api/clusters/1/machines",
                                    data=json.dumps(machines[1]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['id'], 2)
        self.assertEqual(len(response.get_json()['tags']), 2)

        # Actual Operations
        # Delete Operation
        # Check length after deletion
        response = self.client.get("/api/machines/cache")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()['machines']), 0)

        response = self.client.post("/api/machines/cache/stop")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Operation Successful.')

        response = self.client.get("/api/machines/cache")
        self.assertEqual(response.status_code, 200)
        self.assertIs(all(machine['state'] == MachineState.OFF for machine in response.get_json()['machines']), True)

        response = self.client.post("/api/machines/cache/start")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Operation Successful.')

        response = self.client.get("/api/machines/cache")
        self.assertEqual(response.status_code, 200)
        self.assertIs(all(machine['state'] == MachineState.ON for machine in response.get_json()['machines']), True)

        # Delete
        response = self.client.post("/api/machines/cache/delete")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Operation Successful.')

        # Check length after deletion
        response = self.client.get("/api/machines/cache")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['machines']), 0)
