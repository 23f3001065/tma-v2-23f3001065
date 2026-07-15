from flask_restful import Resource, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from extensions import api, db, cache

from models.user import User
from models.trek import Trek
from models.booking import Booking

class TrekkerProfile(Resource):

    @jwt_required()
    def get(self):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'trekker':
            return {
                'msg': 'access denied'
            }, 403

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }, 200

class TrekkerTrekList(Resource):

    @cache.cached(timeout=60)

    @jwt_required()
    def get(self):

        treks = Trek.query.filter_by(
            status='Open'
        ).all()

        return [
            trek.to_json()
            for trek in treks
        ], 200


class TrekkerTrekDetail(Resource):
    @jwt_required()
    def get(self, trek_id):

        trek = Trek.query.get(trek_id)

        if not trek:
            return {'msg': 'trek not found'}, 404

        if trek.status != 'Open':
            return {'msg': 'trek not available'}, 403

        return trek.to_json(), 200


class TrekkerBookingList(Resource):
    @jwt_required()
    def get(self):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'trekker':
            return {
                'msg': 'access denied'
            }, 403

        bookings = Booking.query.filter_by(
            user_id=user.id
        ).all()

        return [

            {
                'id': booking.id,
                'trek_id': booking.trek.id,
                'trek_name': booking.trek.name,
                'location': booking.trek.location,
                'booking_date': str(booking.booking_date),
                'status': booking.status
            }

            for booking in bookings

        ], 200

    @jwt_required()
    def post(self):
        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'trekker':
            return {'msg': 'access denied'}, 403

        data = request.get_json() or {}

        trek = Trek.query.get(
            data.get('trek_id')
        )

        if not trek:
            return {
                'msg': 'trek not found'
            }, 404

        existing_booking = Booking.query.filter_by(
            user_id=user.id,
            trek_id=trek.id
        ).first()

        if existing_booking:
            if existing_booking.status == 'Booked':
                return {
                    'msg': 'you already booked this trek'
                }, 400

            existing_booking.status = 'Booked'
            trek.available_slots -= 1
            db.session.commit()
            cache.clear()

            return {
                'msg': 'booking successful'
            }, 200

        if trek.status != 'Open':
            return {
                'msg': 'trek is not open for booking'
            }, 400

        if trek.available_slots <= 0:
            return {
                'msg': 'no slots available'
            }, 400

        booking = Booking(
            user_id=user.id,
            trek_id=trek.id
        )

        db.session.add(booking)

        trek.available_slots -= 1

        db.session.commit()
        cache.clear()

        return {
            'msg': 'booking successful'
        }, 201

    @jwt_required()
    def put(self):

        from tasks import export_booking_history

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'trekker':
            return {
                'msg': 'access denied'
            }, 403

        export_booking_history.delay(
            user.id
        )

        return {
            'msg': 'Booking history export started. Check your email.'
        }, 200

class TrekkerBookingDetail(Resource):
    def get(self, booking_id):
        return {'msg': f'booking {booking_id} details endpoint'}, 501

    @jwt_required()
    def delete(self, booking_id):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'trekker':
            return {
                'msg': 'access denied'
            }, 403

        booking = Booking.query.get(booking_id)

        if not booking:
            return {
                'msg': 'booking not found'
            }, 404

        if booking.user_id != user.id:
            return {
                'msg': 'access denied'
            }, 403

        if booking.status == 'Cancelled':
            return {
                'msg': 'booking already cancelled'
            }, 400

        booking.status = 'Cancelled'
        booking.trek.available_slots += 1

        db.session.commit()
        cache.clear()

        return {
            'msg': 'booking cancelled'
        }, 200

api.add_resource(TrekkerProfile, '/trekker/profile')
api.add_resource(TrekkerTrekList, '/treks')
api.add_resource(TrekkerTrekDetail, '/treks/<int:trek_id>')
api.add_resource(TrekkerBookingList, '/bookings')
api.add_resource(TrekkerBookingDetail, '/bookings/<int:booking_id>')
