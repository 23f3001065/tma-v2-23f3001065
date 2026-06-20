from flask_restful import Resource, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from extensions import api, db
from models.user import User


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
                'role': u.role
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
            return {'msg': 'name is required'}, 400

        if not email:
            return {'msg': 'email is required'}, 400

        if not password:
            return {'msg': 'password is required'}, 400

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

        return {
            'msg': 'staff created successfully'
        }, 201


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