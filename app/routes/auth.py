from flask import Blueprint
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
from app.models import User
from app import db
from app.api_models import (
    api, user_input, auth_response, login_input,
    error_model, refresh_token_input, refresh_token_response
)

auth_ns = Namespace('auth', description='Authentication operations')
api.add_namespace(auth_ns)

# Access token expires in 15 minutes
ACCESS_EXPIRES = timedelta(minutes=15)
# Refresh token expires in 30 days
REFRESH_EXPIRES = timedelta(days=30)

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(user_input)
    @auth_ns.response(201, 'User created successfully', auth_response)
    @auth_ns.response(422, 'Validation error', error_model)
    def post(self):
        """
        Create a new user account
        
        Returns a user object, access token, and refresh token
        """
        data = auth_ns.payload
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'password_confirmation', 'image_url']
        for field in required_fields:
            if field not in data:
                return {"errors": [f"{field} is required"]}, 422

        if data['password'] != data['password_confirmation']:
            return {"errors": ["Password confirmation doesn't match"]}, 422

        try:
            # Create new user
            user = User(
                username=data['username'],
                email=data['email'],
                image_url=data['image_url']
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()

            # Create tokens
            access_token = create_access_token(
                identity=user.id,
                expires_delta=ACCESS_EXPIRES
            )
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=REFRESH_EXPIRES
            )
            
            return {
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 201

        except ValueError as e:
            return {"errors": [str(e)]}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while creating the user"]}, 500

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_input)
    @auth_ns.response(201, 'Login successful', auth_response)
    @auth_ns.response(401, 'Authentication failed', error_model)
    def post(self):
        """
        Authenticate a user
        
        Returns a user object, access token, and refresh token
        """
        data = auth_ns.payload
        
        if not data.get('username') or not data.get('password'):
            return {"errors": ["Username and password are required"]}, 422

        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(
                identity=user.id,
                expires_delta=ACCESS_EXPIRES
            )
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=REFRESH_EXPIRES
            )
            
            return {
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 201
        
        return {"errors": ["Invalid username or password"]}, 401

@auth_ns.route('/refresh')
class TokenRefresh(Resource):
    @auth_ns.expect(refresh_token_input)
    @auth_ns.response(200, 'Token refresh successful', refresh_token_response)
    @auth_ns.response(401, 'Invalid refresh token', error_model)
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh access token using refresh token
        
        Returns new access token and refresh token
        """
        current_user_id = get_jwt_identity()
        
        # Create new tokens
        access_token = create_access_token(
            identity=current_user_id,
            expires_delta=ACCESS_EXPIRES
        )
        refresh_token = create_refresh_token(
            identity=current_user_id,
            expires_delta=REFRESH_EXPIRES
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200

# Register blueprint
auth_bp = Blueprint('auth', __name__)
