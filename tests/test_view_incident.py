''' 
test module
'''
from flask import json
from  api.view_incident import app
import pytest      

@pytest.fixture()
def client():
    test_client = app.test_client()
    return test_client

class TestViewIncidents:
    '''
    Test the endpoints
    '''
    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_create_new_incident(self, client):
        response = client.post('/api/v1/incidents', data=json.dumps({
             "comment": "Mulyowa is corrupty",
            "createdBy": "mule",
            "createdOn": "2018-12-06 09:52:16.299380",
            "flag_type": "redflag",
            "images": "http/www.com",
            "incident_id": 1,
            "location": "mbale",
            "status": "Draft",
            "videos": "http/url"
        }))
        assert response.status_code == 402  
