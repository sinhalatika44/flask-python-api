from flask import request, Blueprint
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.schemas.user import UserSchema
from app.services.auth_service import AuthService
from app import db, api

auth_ns = Namespace('auth', description='Authentication operations')

user_schema = UserSchema()
auth_service = AuthService()

bp = Blueprint('auth', __name__)

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_schema)
    def post(self):
        """Register a new user"""
        data = request.get_json()
        if auth_service.user_exists(data['username'], data['email']):
            return {"msg": "Username or email already exists"}, 400
        
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        
        return user_schema.dump(new_user), 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_schema)
    def post(self):
        """Login and receive an access token"""
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        return {"msg": "Invalid username or password"}, 401

api.add_namespace(auth_ns)