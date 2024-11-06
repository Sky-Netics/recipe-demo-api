from flask import Blueprint
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db
from app.api_models import api, user_output, error_model
from functools import wraps

users_ns = Namespace('users', description='User operations')
api.add_namespace(users_ns)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or not current_user.is_admin():
            return {"errors": ["Admin access required"]}, 403
        return fn(*args, **kwargs)
    return wrapper

@users_ns.route('/users')
class UserList(Resource):
    @jwt_required()
    @admin_required
    @users_ns.doc(security='Bearer Auth')
    @users_ns.response(200, 'Success', [user_output])
    @users_ns.response(403, 'Admin access required', error_model)
    def get(self):
        """Get all users (Admin only)"""
        users = User.query.all()
        return [user.to_dict() for user in users], 200

@users_ns.route('/me')
class UserMe(Resource):
    @jwt_required()
    @users_ns.doc(security='Bearer Auth')
    @users_ns.response(200, 'Success', user_output)
    @users_ns.response(404, 'User not found', error_model)
    def get(self):
        """Get current user's details"""
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
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
        current_user = User.query.get(current_user_id)
        
        # Allow admin to update any user, but regular users can only update themselves
        if not current_user.is_admin() and current_user_id != id:
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
            # Only admin can update roles
            if 'role' in data and current_user.is_admin():
                user.role = data['role']

            db.session.commit()
            return user.to_dict(), 200

        except ValueError as e:
            return {"errors": [str(e)]}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while updating the user"]}, 500

# Register blueprint
users_bp = Blueprint('users', __name__)
