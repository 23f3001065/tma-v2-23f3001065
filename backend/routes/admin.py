from models.staff_profile import StaffProfile
from datetime import date

from flask_restful import Resource, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from extensions import api, db, cache

from models.user import User
from models.trek import Trek
from models.booking import Booking


class AdminDashboard(Resource):

    @cache.cached(timeout=60)

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        total_users = User.query.count()

        total_staff = User.query.filter_by(
            role='staff'
        ).count()

        total_treks = Trek.query.count()

        total_bookings = Booking.query.count()

        return {
            'total_users': total_users,
            'total_staff': total_staff,
            'total_treks': total_treks,
            'total_bookings': total_bookings
        }, 200


class AdminUserList(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        users = User.query.all()

        return [
            {
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'role': u.role,
                'is_active': u.is_active
            }
            for u in users
        ], 200

    @jwt_required()
    def post(self):

        user_id = get_jwt_identity()

        admin = User.query.get(user_id)

        if admin.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        data = request.get_json() or {}

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name:
            return {
                'msg': 'name is required'
            }, 400

        if not email:
            return {
                'msg': 'email is required'
            }, 400

        if not password:
            return {
                'msg': 'password is required'
            }, 400

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return {
                'msg': 'email already registered'
            }, 400

        staff = User(
            name=name,
            email=email,
            password=password,
            role='staff',
            is_active=True
        )

        db.session.add(staff)
        db.session.commit()

        staff_profile = StaffProfile(
            user_id=staff.id
        )

        db.session.add(staff_profile)
        db.session.commit()

        return {
            'msg': 'staff created successfully'
        }, 201


class AdminTrekList(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        treks = Trek.query.all()

        return [
            trek.to_json()
            for trek in treks
        ], 200

    @jwt_required()
    def post(self):

        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        data = request.get_json() or {}

        start_date = date.fromisoformat(
            data['start_date']
        )

        end_date = date.fromisoformat(
            data['end_date']
        )

        if end_date < start_date:
            return {
                'msg': 'end date must be after start date'
            }, 400

        if data['available_slots'] < 0:
            return {
                'msg': 'available slots cannot be negative'
            }, 400

        trek = Trek(
            name=data['name'],
            location=data['location'],
            difficulty=data['difficulty'],
            duration_days=data['duration_days'],
            description=data['description'],
            available_slots=data['available_slots'],
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(trek)
        db.session.commit()
        cache.clear()

        return {
            'msg': 'trek created successfully'
        }, 201

class AdminUserDetail(Resource):

    @jwt_required()
    def put(self, user_id):

        admin = User.query.get(
            get_jwt_identity()
        )

        if admin.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        user = User.query.get(user_id)

        if not user:
            return {
                'msg': 'user not found'
            }, 404

        data = request.get_json() or {}

        user.is_active = data.get(
            'is_active',
            user.is_active
        )

        db.session.commit()

        if user.is_active:

            msg = 'user activated'

        else:

            msg = 'user deactivated'

        return {
            'msg': msg
        }, 200


class AdminTrekDetail(Resource):

    @jwt_required()
    def put(self, trek_id):

        admin = User.query.get(
            get_jwt_identity()
        )

        if admin.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        trek = Trek.query.get(trek_id)

        if not trek:
            return {
                'msg': 'trek not found'
            }, 404

        data = request.get_json() or {}

        start_date = date.fromisoformat(
            data.get(
                'start_date',
                str(trek.start_date)
            )
        )

        end_date = date.fromisoformat(
            data.get(
                'end_date',
                str(trek.end_date)
            )
        )

        if end_date < start_date:
            return {
                'msg': 'end date must be after start date'
            }, 400

        available_slots = data.get(
            'available_slots',
            trek.available_slots
        )

        if available_slots < 0:
            return {
                'msg': 'available slots cannot be negative'
            }, 400

        trek.name = data.get(
            'name',
            trek.name
        )

        trek.location = data.get(
            'location',
            trek.location
        )

        trek.difficulty = data.get(
            'difficulty',
            trek.difficulty
        )

        trek.duration_days = data.get(
            'duration_days',
            trek.duration_days
        )

        trek.description = data.get(
            'description',
            trek.description
        )

        trek.available_slots = available_slots

        trek.start_date = start_date

        trek.end_date = end_date

        trek.status = data.get(
            'status',
            trek.status
        )

        db.session.commit()
        cache.clear()

        return {
            'msg': 'trek updated'
        }, 200

    @jwt_required()
    def delete(self, trek_id):

        admin = User.query.get(
            get_jwt_identity()
        )

        if admin.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        trek = Trek.query.get(trek_id)

        if not trek:
            return {
                'msg': 'trek not found'
            }, 404

        db.session.delete(trek)

        db.session.commit()
        cache.clear()

        return {
            'msg': 'trek deleted'
        }, 200


class AdminAssignStaff(Resource):

    @jwt_required()
    def put(self, trek_id):

        admin = User.query.get(
            get_jwt_identity()
        )

        if admin.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        trek = Trek.query.get(trek_id)

        if not trek:
            return {
                'msg': 'trek not found'
            }, 404

        data = request.get_json() or {}

        staff_id = data.get('staff_id')

        staff = User.query.get(staff_id)

        if not staff:
            return {
                'msg': 'staff not found'
            }, 404

        if staff.role != 'staff':
            return {
                'msg': 'user is not staff'
            }, 400

        staff_profile = StaffProfile.query.filter_by(
            user_id=staff.id
        ).first()

        if not staff_profile:
            return {
                'msg': 'staff profile not found'
            }, 404

        trek.staff_id = staff_profile.id

        db.session.commit()
        cache.clear()

        return {
            'msg': 'staff assigned'
        }, 200

class AdminBookingList(Resource):

    @jwt_required()
    def get(self):

        user = User.query.get(
            get_jwt_identity()
        )

        if user.role != 'admin':
            return {
                'msg': 'access denied'
            }, 403

        bookings = Booking.query.all()

        return [

            {
                'booking_id': booking.id,
                'trekker_name': booking.user.name,
                'email': booking.user.email,
                'trek_name': booking.trek.name,
                'location': booking.trek.location,
                'booking_date': str(booking.booking_date),
                'status': booking.status
            }

            for booking in bookings

        ], 200


api.add_resource(
    AdminDashboard,
    '/admin/dashboard'
)

api.add_resource(
    AdminUserList,
    '/admin/users'
)

api.add_resource(
    AdminTrekList,
    '/admin/treks'
)

api.add_resource(
    AdminBookingList,
    '/admin/bookings'
)

api.add_resource(
    AdminUserDetail,
    '/admin/users/<int:user_id>'
)

api.add_resource(
    AdminTrekDetail,
    '/admin/treks/<int:trek_id>'
)

api.add_resource(
    AdminAssignStaff,
    '/admin/treks/<int:trek_id>/assign-staff'
)