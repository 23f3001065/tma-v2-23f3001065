from flask_restful import Resource
from extensions import api


class StaffProfile(Resource):
    def get(self):
        return {'msg': 'get staff profile endpoint'}, 501
    
    def put(self):
        return {'msg': 'update staff profile endpoint'}, 501


class StaffTreks(Resource):
    def get(self):
        return {'msg': 'list staff treks endpoint'}, 501
    
    def post(self):
        return {'msg': 'create trek endpoint'}, 501


class StaffTrekBookings(Resource):
    def get(self, trek_id):
        return {'msg': f'list bookings for trek {trek_id} endpoint'}, 501


api.add_resource(StaffProfile, '/staff/profile')
api.add_resource(StaffTreks, '/staff/treks')
api.add_resource(StaffTrekBookings, '/staff/treks/<int:trek_id>/bookings')
