from flask_restful import Resource
from extensions import api


class AdminUserList(Resource):
    def get(self):
        return {'msg': 'list users endpoint'}, 501
    
    def post(self):
        return {'msg': 'create user endpoint'}, 501


class AdminTrekList(Resource):
    def get(self):
        return {'msg': 'list treks endpoint'}, 501
    
    def post(self):
        return {'msg': 'create trek endpoint'}, 501


class AdminBookingList(Resource):
    def get(self):
        return {'msg': 'list bookings endpoint'}, 501


api.add_resource(AdminUserList, '/admin/users')
api.add_resource(AdminTrekList, '/admin/treks')
api.add_resource(AdminBookingList, '/admin/bookings')
