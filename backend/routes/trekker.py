from flask_restful import Resource
from extensions import api


class TrekkerTrekList(Resource):
    def get(self):
        return {'msg': 'list available treks endpoint'}, 501


class TrekkerTrekDetail(Resource):
    def get(self, trek_id):
        return {'msg': f'trek {trek_id} details endpoint'}, 501


class TrekkerBookingList(Resource):
    def get(self):
        return {'msg': 'list user bookings endpoint'}, 501
    
    def post(self):
        return {'msg': 'create booking endpoint'}, 501


class TrekkerBookingDetail(Resource):
    def get(self, booking_id):
        return {'msg': f'booking {booking_id} details endpoint'}, 501
    
    def delete(self, booking_id):
        return {'msg': f'cancel booking {booking_id} endpoint'}, 501


api.add_resource(TrekkerTrekList, '/treks')
api.add_resource(TrekkerTrekDetail, '/treks/<int:trek_id>')
api.add_resource(TrekkerBookingList, '/bookings')
api.add_resource(TrekkerBookingDetail, '/bookings/<int:booking_id>')
