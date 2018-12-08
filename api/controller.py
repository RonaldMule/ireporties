from flask import request, jsonify, json
from api.incident_model import Incident, IncidentDb, Base_Incident
from api.utilities import IncidentValidator

#conn_db = IncidentDb()

class IncidentController():
    def __init__(self):
        self.conn_db = IncidentDb()
        
  
    def create_incident(self):
        data = request.get_json()
        incident_id = data.get("incident_id")
        createdBy = data.get("createdBy")
        createdOn = data.get("created_on")
        flag_type = data.get("flag_type")
        location = data.get("location")
        status = data.get("status")
        images = data.get("images")
        videos = data.get("videos")
        comment = data.get("comment")
      
        #validation of user input
    
       
        if not  IncidentValidator.validate_status(status):
            return jsonify ({'status': 400,
                            'error': 'The status provided is not defined'
        })
        if not IncidentValidator.validate_flag_type(flag_type):
            return jsonify ({'status': 400,
                            'error': 'The flag_type is not defined'
            })
       

        incident = Incident(Base_Incident(createdOn, createdBy, 
         flag_type, location), status, images, videos, comment)
        
        self.conn_db.add_incident(incident)
        #incident = new_incindent.to_json()
        return jsonify({
            "status": 201,
            'data':[{
                'incident_id':incident.incident_id,
             "message": f"created {flag_type} "}]
                
            }), 201

    def get_mall_incidents(self):
        '''geting all incidents '''
        return jsonify ({'status':200, 
                        'data':self.conn_db.get_incident_json()
        }),200

    def get_a_specific_incident(self,incident_id ):
        response = self.conn_db.get_incident_by_id(incident_id)
        if response:
            return jsonify({'data':response})
        return jsonify({'message': 'No incident found '}) 

    def delete_a_specific_incident(self, incident_id):
        ren = self.conn_db.get_incident_by_id(incident_id)
        if ren:
            self.conn_db.incident_list.remove(ren)
            return jsonify({'message': 'removed successfully'})
            
            
        return jsonify({'message': 'no items to delete'})    






    
    def update_location(self, incident_id):
        response = self.conn_db.get_incident_by_id(incident_id)
        if response:
            data = request.get_json()
            #status = data.get('status')
            if response['status'] == 'Draft':
                self.conn_db.get_incident_by_id(incident_id).update(location = data['location'])
                

                return jsonify({'message': 'update location was successfully made'})
            return jsonify({'message': 'you can not update that please'})  
        return jsonify({'message':" no incidents currently"})  

    def update_comment(self, incident_id):

        response = self.conn_db.get_incident_by_id(incident_id)
        if response:
            data = request.get_json()
            if response['status'] == 'Draft':
                
                self.conn_db.get_incident_by_id(incident_id).update(comment = data['comment'])
                return jsonify({'message': 'comment successfully updated'})
            return jsonify({'message': 'you can not update that please'})  
        return jsonify({'message':" no incidents currently"})  
