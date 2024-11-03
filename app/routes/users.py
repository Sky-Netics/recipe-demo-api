from flask import Blueprint
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db
from app.api_models import api, user_output, error_model

users_ns = Namespace('users', description='User operations')
api.add_namespace(users_ns)

@users_ns.route('/users')
class UserList(Resource):
    @users_ns.response(200, 'Success', [user_output])
    def get(self):
        """Get all users"""
        users = User.query.all()
        return [user.to_dict() for user in users], 200

@users_ns.route('/me/<int:id>')
class UserDetail(Resource):
    @jwt_required()
    @users_ns.doc(security='Bearer Auth')
    @users_ns.response(200, 'Success', user_output)
    @users_ns.response(404, 'User not found', error_model)
    def get(self, id):
        """Get a specific user's details"""
        user = User.query.get_or_404(id)
        return user.to_dict(), 200

@users_ns.route('/users/<int:id>')
class UserUpdate(Resource):
    @jwt_required()
    @users_ns.doc(security='Bearer Auth')
    @users_ns.doc(params={'id': 'The user ID'})
    @users_ns.response(200, 'User updated successfully', user_output)
    @users_ns.response(401, 'Not authorized', error_model)
    @users_ns.response(404, 'User not found', error_model)
    @users_ns.response(422, 'Validation error', error_model)
    def patch(self, id):
        """Update a user's information"""
        current_user_id = get_jwt_identity()
        if current_user_id != id:
            return {"errors": ["Not authorized"]}, 401

        user = User.query.get_or_404(id)
        data = users_ns.payload

        try:
            # Update fields if they are present in the request
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'image_url' in data:
                user.image_url = data['image_url']

            db.session.commit()
            return user.to_dict(), 200

        except ValueError as e:
            return {"errors": [str(e)]}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while updating the user"]}, 500

# Register blueprint
users_bp = Blueprint('users', __name__)
