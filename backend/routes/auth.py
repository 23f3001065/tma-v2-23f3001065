from models.user import User
from flask_restful import Resource, request
from extensions import db, api
from flask_jwt_extended import create_access_token


class Register(Resource):
    def post(self):
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

        user = User.query.filter_by(email=email).first()

        if user:
            return {'msg': 'email already registered'}, 400

        user = User(name=name, email=email, password=password, role='trekker', is_active=True)

        db.session.add(user)
        db.session.commit()

        return {
            'msg': 'user registered successfully!'
        }, 201


class Login(Resource):
    def post(self):
        data = request.get_json() or {}

        email = data.get('email')
        password = data.get('password')

        if not email:
            return {'msg': 'email is required'}, 400

        if not password:
            return {'msg': 'password is required'}, 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return {'msg': 'no such user exists'}, 404

        if not user.is_active:
            return {'msg': 'account is inactive'}, 403

        if user.password != password:
            return {'msg': 'incorrect password'}, 401

        access_token = create_access_token(identity=str(user.id))

        return {
            'msg': 'logged in successfully',
            'access_token': access_token,
            'role': user.role
        }, 200


api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')

