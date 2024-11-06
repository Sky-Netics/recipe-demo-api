from flask import Blueprint, request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Recipe
from app import db
from app.api_models import api, recipe_input, recipe_output, error_model

recipes_ns = Namespace('recipes', description='Recipe operations')
api.add_namespace(recipes_ns)

@recipes_ns.route('/recipes')
class RecipeList(Resource):
    @recipes_ns.response(200, 'Success', [recipe_output])
    @recipes_ns.doc(params={
        'page': 'Page number (default: 1)',
        'per_page': 'Items per page (default: 10)'
    })
    def get(self):
        """Get all recipes with pagination"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Ensure valid pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10

        pagination = Recipe.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return {
            'items': [recipe.to_dict() for recipe in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }, 200

    @jwt_required()
    @recipes_ns.doc(security='Bearer Auth')
    @recipes_ns.expect(recipe_input)
    @recipes_ns.response(201, 'Recipe created successfully', recipe_output)
    @recipes_ns.response(422, 'Validation error', error_model)
    def post(self):
        """Create a new recipe"""
        current_user_id = get_jwt_identity()
        data = recipes_ns.payload

        try:
            # Add current user_id to recipe data
            data['user_id'] = current_user_id
            
            # Create new recipe
            recipe = Recipe(**data)
            db.session.add(recipe)
            db.session.commit()

            return recipe.to_dict(), 201

        except ValueError as e:
            return {"errors": [str(e)]}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while creating the recipe"]}, 500

@recipes_ns.route('/my-recipes')
class MyRecipes(Resource):
    @jwt_required()
    @recipes_ns.doc(security='Bearer Auth')
    @recipes_ns.response(200, 'Success', [recipe_output])
    @recipes_ns.doc(params={
        'page': 'Page number (default: 1)',
        'per_page': 'Items per page (default: 10)'
    })
    def get(self):
        """Get current user's recipes with pagination"""
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Ensure valid pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10

        pagination = Recipe.query.filter_by(user_id=current_user_id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return {
            'items': [recipe.to_dict() for recipe in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }, 200

@recipes_ns.route('/recipes/<int:id>')
class RecipeDetail(Resource):
    @recipes_ns.response(200, 'Success', recipe_output)
    @recipes_ns.response(404, 'Recipe not found', error_model)
    def get(self, id):
        """Get a specific recipe"""
        recipe = Recipe.query.get_or_404(id)
        return recipe.to_dict(), 200

    @jwt_required()
    @recipes_ns.doc(security='Bearer Auth')
    @recipes_ns.expect(recipe_input)
    @recipes_ns.response(200, 'Recipe updated successfully', recipe_output)
    @recipes_ns.response(401, 'Not authorized', error_model)
    @recipes_ns.response(404, 'Recipe not found', error_model)
    @recipes_ns.response(422, 'Validation error', error_model)
    def patch(self, id):
        """Update a recipe"""
        current_user_id = get_jwt_identity()
        recipe = Recipe.query.get_or_404(id)

        # Check if the current user owns the recipe
        if recipe.user_id != current_user_id:
            return {"errors": ["Not authorized to update this recipe"]}, 401

        try:
            data = recipes_ns.payload
            
            # Update recipe fields
            for key, value in data.items():
                if hasattr(recipe, key):
                    setattr(recipe, key, value)

            db.session.commit()
            return recipe.to_dict(), 200

        except ValueError as e:
            return {"errors": [str(e)]}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while updating the recipe"]}, 500

    @jwt_required()
    @recipes_ns.doc(security='Bearer Auth')
    @recipes_ns.response(204, 'Recipe deleted successfully')
    @recipes_ns.response(401, 'Not authorized', error_model)
    @recipes_ns.response(404, 'Recipe not found', error_model)
    def delete(self, id):
        """Delete a recipe"""
        current_user_id = get_jwt_identity()
        recipe = Recipe.query.get_or_404(id)

        # Check if the current user owns the recipe
        if recipe.user_id != current_user_id:
            return {"errors": ["Not authorized to delete this recipe"]}, 401

        try:
            db.session.delete(recipe)
            db.session.commit()
            return '', 204

        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while deleting the recipe"]}, 500

# Register blueprint
recipes_bp = Blueprint('recipes', __name__)
