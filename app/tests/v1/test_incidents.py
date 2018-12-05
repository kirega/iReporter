"""
    This file contains all tests for the incidents API
    It tests for all GET,POST, PATCH and DELETE functions in the incident API
"""
import unittest
from flask import json
from ... import create_app
from .basetest import BaseTestCase
app = create_app()


class IncidentsTest(BaseTestCase):
 
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
        data  = json.loads(result.data)
        self.assertEqual(data['data']["incidentId"], 1)

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
        result = self.app.put('/api/v1/incident/1000/comment', data=data)
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Update on non-existing record denied")
    
    def test_update_on_with_wrong_format(self):
        data = json.dumps({"comment": "Too many potholes",
                          })
        result = self.app.put('/api/v1/incident/1/comment', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Comment/userid is not present")

    def test_update_with_empty_values(self):
        data = json.dumps({})
        result = self.app.put('/api/v1/incident/1/location', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "location/userid is not present")

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
