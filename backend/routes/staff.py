from flask_restful import Resource, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from extensions import api, db

from models.user import User
from models.staff_profile import StaffProfile
from models.trek import Trek
from models.booking import Booking


class StaffProfileResource(Resource):

    @jwt_required()
    def get(self):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'staff':
            return {
                'msg': 'access denied'
            }, 403

        staff_profile = StaffProfile.query.filter_by(
            user_id=user.id
        ).first()

        if not staff_profile:
            return {
                'msg': 'staff profile not found'
            }, 404

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'contact_no': staff_profile.contact_no,
            'experience_years': staff_profile.experience_years,
            'status': staff_profile.status
        }, 200
    
    def put(self):
        return {'msg': 'update staff profile endpoint'}, 501


class StaffTreks(Resource):
    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "staff":
            return {
                "msg": "access denied"
            }, 403

        staff_profile = StaffProfile.query.filter_by(
            user_id=user.id
        ).first()

        if not staff_profile:
            return {
                "msg": "staff profile not found"
            }, 404

        treks = Trek.query.filter_by(
            staff_id=staff_profile.id
        ).all()

        return [
            trek.to_json()
            for trek in treks
        ], 200

    def post(self):
        return {'msg': 'create trek endpoint'}, 501

class StaffTrekDetail(Resource):

    @jwt_required()
    def get(self, trek_id):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'staff':
            return {
                'msg': 'access denied'
            }, 403

        staff_profile = StaffProfile.query.filter_by(
            user_id=user.id
        ).first()

        if not staff_profile:
            return {
                'msg': 'staff profile not found'
            }, 404

        trek = Trek.query.get(trek_id)

        if not trek:
            return {
                'msg': 'trek not found'
            }, 404

        if trek.staff_id != staff_profile.id:
            return {
                'msg': 'this trek is not assigned to you'
            }, 403

        return trek.to_json(), 200
    
    @jwt_required()
    def put(self, trek_id):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'staff':
            return {
                'msg': 'access denied'
            }, 403

        staff_profile = StaffProfile.query.filter_by(
            user_id=user.id
        ).first()

        if not staff_profile:
            return {
                'msg': 'staff profile not found'
            }, 404

        trek = Trek.query.get(trek_id)

        if not trek:
            return {
                'msg': 'trek not found'
            }, 404

        if trek.staff_id != staff_profile.id:
            return {
                'msg': 'this trek is not assigned to you'
            }, 403

        data = request.get_json() or {}

        trek.available_slots = data.get(
            'available_slots',
            trek.available_slots
        )

        trek.status = data.get(
            'status',
            trek.status
        )

        db.session.commit()

        return {
            'msg': 'trek updated'
        }, 200

class StaffTrekBookings(Resource):
    @jwt_required()
    def get(self, trek_id):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'staff':
            return {
                'msg': 'access denied'
            }, 403

        staff_profile = StaffProfile.query.filter_by(
            user_id=user.id
        ).first()

        if not staff_profile:
            return {
                'msg': 'staff profile not found'
            }, 404

        trek = Trek.query.get(trek_id)

        if not trek:
            return {
                'msg': 'trek not found'
            }, 404

        if trek.staff_id != staff_profile.id:
            return {
                'msg': 'this trek is not assigned to you'
            }, 403

        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status='Booked'
        ).all()

        return [

            {
                'booking_id': booking.id,
                'user_id': booking.user.id,
                'name': booking.user.name,
                'email': booking.user.email,
                'status': booking.status
            }

            for booking in bookings

        ], 200

api.add_resource(StaffProfileResource, '/staff/profile')
api.add_resource(StaffTreks, '/staff/treks')
api.add_resource(StaffTrekBookings, '/staff/treks/<int:trek_id>/bookings')
api.add_resource(StaffTrekDetail, '/staff/treks/<int:trek_id>')