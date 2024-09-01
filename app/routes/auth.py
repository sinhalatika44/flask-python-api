from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.schemas.user import UserSchema
from app.services.auth_service import AuthService
from app import db

bp = Blueprint('auth', __name__)
user_schema = UserSchema()
auth_service = AuthService()

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if auth_service.user_exists(data['username'], data['email']):
        return jsonify({"msg": "Username or email already exists"}), 400
    
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.dump(new_user), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid username or password"}), 401