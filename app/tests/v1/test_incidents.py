"""
    This file contains all tests for the incidents API
    It tests for all GET,POST, PATCH and DELETE functions in the incident API
"""
import unittest
from flask import json
from ... import create_app

app = create_app()


class IncidentsTest(unittest.TestCase):
    def setUp(self):
        """
        Initializing the reusable part.
        """
        self.app = app.test_client()
        self.app.testing = True
        image_in_base64 = "data:image/png;base64,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"
        new_incident_data = {
            "comment": "Police taking a bribe",
            "incidentType": "red-flag",
            "location": "-1.28333, 36.81667",
            "createdBy": 1,
            "images": [image_in_base64, image_in_base64],
            "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                       "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
        }
        new_incident_data_nonexisting_user = {
            "comment": "Police taking a bribe",
            "incidentType": "red-flag",
            "location": "-1.28333, 36.81667",
            "createdBy": 100,
            "images": [image_in_base64, image_in_base64],
            "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                       "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
        }
        new_incident_data_with_wrong_format = {
            "comment": "Police taking a bribe",
            "incidntType": "red-flag",
            "location": "-1.28333, 36.81667",
            "createdBy": 1,
            "images": [image_in_base64, image_in_base64],
            "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                       "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
        }
        self.new_incident = json.dumps(new_incident_data)
        self.new_incident_data_with_wrong_format = json.dumps(
            new_incident_data_with_wrong_format)
        self.new_incident_data_nonexisting_user = json.dumps(
            new_incident_data_nonexisting_user)

    def test_create_new_incident(self):
        result = self.app.post('/api/v1/incidents', data=self.new_incident)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "New incident created")

    def test_create_new_incident_with_wrong_format(self):
        result = self.app.post('/api/v1/incidents',
                               data=self.new_incident_data_with_wrong_format)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_get_all_incidents(self):
        result = self.app.get('/api/v1/incidents')
        self.assertEqual(result.status_code, 200)

    def test_create_new_incident_user_doesnt_exist(self):
        result = self.app.post('/api/v1/incidents',
                               data=self.new_incident_data_nonexisting_user)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Not Authorized")

    def test_get_specific_incident(self):
        result = self.app.get("/api/v1/incident/1")
        self.assertEqual(result.status_code, 200)

    def test_get_non_existing_record(self):
        result = self.app.get("/api/v1/incident/1000")
        self.assertEqual(result.status_code, 404)

    def test_update_an_incident_location(self):
        data = json.dumps({"location": "-1.28333, 36.81667",
                           "userid": 1})
        result = self.app.put('/api/v1/incident/1/location', data=data)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Incident Updated")

    def test_update_an_incident_comment(self):
        data = json.dumps({"comment": "Too many potholes",
                           "userid": 1})
        result = self.app.put('/api/v1/incident/1/comment', data=data)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Incident Updated")

    def test_update_on_nonexisting_incident(self):
        data = json.dumps({"comment": "Too many potholes",
                           "userid": 1})
        result = self.app.put('/api/v1/incident/1000/location', data=data)
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Update on non-existing record denied")
    # TODO :: REWRITE THIS TEST

    def test_update_with_empty_values(self):
        data = json.dumps({})
        result = self.app.put('/api/v1/incident/1/location', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Empty payload")

    def test_update_on_incident_not_in_draft(self):
        """Test that an incident that is not in draft cannot be 
        edited except to change the status"""
        data = json.dumps({"comment": "Too many potholes",
                           "userid": 2})
        result = self.app.put('/api/v1/incident/2/comment', data=data)
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Cannot update a record not in draft state")

    def test_update_user_didnt_create_comment(self):
        """"Tests that only user who created can update the record"""
        data = json.dumps({"comment": "Too many potholes",
                           "userid": 2})
        result = self.app.put('/api/v1/incident/1/comment', data=data)
        self.assertEqual(result.status_code, 403)

# DELETE AN INCIDENT TESTS
    def test_delete_incident(self):
        result = self.app.delete('/api/v1/incident/3',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(data["status"], 204)
        self.assertEqual(data['message'], "Incident record has been deleted")

    def test_delete_incident_with_wrong_user(self):
        result = self.app.delete('/api/v1/incident/2',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['message'], "Forbidden: Record not owned")

    def test_delete_incident_with_missing_field(self):
        result = self.app.delete('/api/v1/incident/2',
                            data=json.dumps({}))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'],"Missing userid field")
    def test_delete_nonexisting_incident(self):
        result = self.app.delete('/api/v1/incident/1000',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['message'], "Incident does not exist")
if __name__ == '__main__':
    unittest.main()
